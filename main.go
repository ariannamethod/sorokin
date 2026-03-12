package main

/*
#cgo CFLAGS: -DSOROKIN_LIB
#cgo LDFLAGS: -lm
#include "sorokin.h"
#include <stdlib.h>
#include <string.h>

extern void sorokin_init(void);
extern void sorokin_set_mutation_provider(mutation_provider_fn fn);
extern void run_autopsy(const char *prompt);

// nano_bridge_shim defined in bridge.c
extern int nano_bridge_shim(const char *word,
    char results[][MAX_WORD_LEN], int max_results);
*/
import "C"

import (
	"bufio"
	"fmt"
	"math"
	"math/rand"
	"os"
	"strings"
	"time"
	"unsafe"
)

// EmbedProvider finds semantically related words via embedding cosine similarity.
// No forward passes — just one matmul against the embedding table.
// Dead words attracted to living ones by the geometry of latent space.
type EmbedProvider struct {
	tokenizer *Tokenizer
	embedData []byte   // raw embedding weights
	embedType uint32   // tensor type
	dim       int      // embedding dimension
	vocab     int      // vocab size
	norms     []float32 // precomputed L2 norms per token
	rng       *rand.Rand
}

var (
	provider *EmbedProvider
)

func NewEmbedProvider(modelPath string) (*EmbedProvider, error) {
	if _, err := os.Stat(modelPath); err != nil {
		return nil, fmt.Errorf("model not found: %s", modelPath)
	}

	fmt.Fprintf(os.Stderr, "[embed] loading %s...\n", modelPath)

	gguf, err := LoadGGUF(modelPath)
	if err != nil {
		return nil, fmt.Errorf("GGUF load: %v", err)
	}

	tokenizer := NewTokenizer(&gguf.Meta)
	dim := gguf.Meta.EmbedDim
	vocab := gguf.Meta.VocabSize

	embData, embInfo, err := gguf.GetTensor("token_embd.weight")
	if err != nil {
		return nil, fmt.Errorf("token_embd.weight: %v", err)
	}

	ep := &EmbedProvider{
		tokenizer: tokenizer,
		embedData: embData,
		embedType: embInfo.Type,
		dim:       dim,
		vocab:     vocab,
		rng:       rand.New(rand.NewSource(time.Now().UnixNano())),
	}

	// Precompute L2 norms for all tokens
	t0 := time.Now()
	ep.norms = make([]float32, vocab)
	buf := make([]float32, dim)
	for i := 0; i < vocab; i++ {
		embedLookupInto(buf, ep.embedData, ep.embedType, i, dim)
		var ss float64
		for _, v := range buf {
			ss += float64(v) * float64(v)
		}
		ep.norms[i] = float32(math.Sqrt(ss))
	}
	fmt.Fprintf(os.Stderr, "[embed] norms precomputed in %v\n", time.Since(t0))

	fmt.Fprintf(os.Stderr, "[embed] ready — %d vocab, %d dim, type=%s\n",
		vocab, dim, typeName(embInfo.Type))

	return ep, nil
}

// getEmbedding retrieves the embedding for a word.
// Multi-token words: average their embeddings.
func (ep *EmbedProvider) getEmbedding(word string) []float32 {
	tokens := ep.tokenizer.Encode(word, false)
	if len(tokens) == 0 {
		return nil
	}

	emb := make([]float32, ep.dim)
	buf := make([]float32, ep.dim)

	for _, tok := range tokens {
		if tok < 0 || tok >= ep.vocab {
			continue
		}
		embedLookupInto(buf, ep.embedData, ep.embedType, tok, ep.dim)
		for i := range emb {
			emb[i] += buf[i]
		}
	}

	// Normalize (average already baked into the norm comparison)
	if len(tokens) > 1 {
		inv := 1.0 / float32(len(tokens))
		for i := range emb {
			emb[i] *= inv
		}
	}
	return emb
}

// FindNeighbors returns top-K nearest words by cosine similarity.
// Skips subword tokens, punctuation, and the input word itself.
func (ep *EmbedProvider) FindNeighbors(word string, maxResults int) []string {
	emb := ep.getEmbedding(word)
	if emb == nil {
		return nil
	}

	// Query norm
	var qnorm float64
	for _, v := range emb {
		qnorm += float64(v) * float64(v)
	}
	qnorm = math.Sqrt(qnorm)
	if qnorm < 1e-10 {
		return nil
	}

	// Cosine similarity against all tokens
	type scored struct {
		idx   int
		score float32
	}

	// Oversample: get 4x candidates, then filter for real words
	topK := maxResults * 4
	if topK < 32 {
		topK = 32
	}
	top := make([]scored, topK)
	for i := range top {
		top[i] = scored{-1, -2}
	}

	buf := make([]float32, ep.dim)
	lowWord := strings.ToLower(word)

	for i := 0; i < ep.vocab; i++ {
		if ep.norms[i] < 1e-10 {
			continue
		}

		embedLookupInto(buf, ep.embedData, ep.embedType, i, ep.dim)
		var dot float64
		for d := 0; d < ep.dim; d++ {
			dot += float64(emb[d]) * float64(buf[d])
		}
		sim := float32(dot / (qnorm * float64(ep.norms[i])))

		if sim > top[topK-1].score {
			top[topK-1] = scored{i, sim}
			// Bubble up
			for j := topK - 1; j > 0 && top[j].score > top[j-1].score; j-- {
				top[j], top[j-1] = top[j-1], top[j]
			}
		}
	}

	// Filter: only real words (3+ alpha chars, no subword markers)
	seen := map[string]bool{lowWord: true}
	var results []string
	for _, s := range top {
		if s.idx < 0 {
			continue
		}
		piece := ep.tokenizer.DecodeToken(s.idx)
		piece = strings.TrimSpace(piece)
		clean := strings.ToLower(piece)

		// Skip subwords (▁ prefix means beginning of word in SentencePiece)
		// Keep words that start with ▁ but strip the prefix
		if strings.HasPrefix(clean, "\u2581") {
			clean = clean[len("\u2581"):]
		}

		// Must be pure alpha, 3+ chars
		if len(clean) < 3 || !isAlpha(clean) {
			continue
		}
		if seen[clean] {
			continue
		}
		seen[clean] = true
		results = append(results, clean)
		if len(results) >= maxResults {
			break
		}
	}

	return results
}

func isAlpha(s string) bool {
	for _, c := range s {
		if !((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) {
			return false
		}
	}
	return true
}

// nanoMutationBridge is the CGO callback — called from C's get_mutations()
//
//export nanoMutationBridge
func nanoMutationBridge(word *C.char, results unsafe.Pointer, maxResults C.int) C.int {
	if provider == nil {
		return 0
	}

	goWord := C.GoString(word)
	mutations := provider.FindNeighbors(goWord, int(maxResults))

	n := 0
	for _, m := range mutations {
		if n >= int(maxResults) {
			break
		}
		dst := (*[64]byte)(unsafe.Pointer(uintptr(results) + uintptr(n*64)))
		if len(m) > 63 {
			m = m[:63]
		}
		copy(dst[:], m)
		dst[len(m)] = 0
		n++
	}
	return C.int(n)
}

func main() {
	// Quantize mode: ./sorokin -quantize input.gguf output.gguf
	if len(os.Args) >= 4 && os.Args[1] == "-quantize" {
		fmt.Printf("[quantize] %s → %s\n", os.Args[2], os.Args[3])
		if err := QuantizeGGUF(os.Args[2], os.Args[3]); err != nil {
			fmt.Fprintf(os.Stderr, "quantize failed: %v\n", err)
			os.Exit(1)
		}
		fmt.Printf("[quantize] done\n")
		return
	}

	// Initialize C-side autopsy engine
	C.sorokin_init()

	// Look for nanollama GGUF model (prefer q4_0 — smaller footprint)
	modelPaths := []string{
		"nano-base-q4_0.gguf",
		"nano-base-f16.gguf",
		os.Getenv("HOME") + "/Downloads/nanollama/weights/nano-base-q4_0.gguf",
		os.Getenv("HOME") + "/Downloads/nanollama/weights/nano-base-f16.gguf",
		os.Getenv("HOME") + "/Downloads/nanollama/weights/nano-f16.gguf",
		"../nanollama/weights/nano-base-f16.gguf",
	}

	var modelPath string
	for _, p := range modelPaths {
		if _, err := os.Stat(p); err == nil {
			modelPath = p
			break
		}
	}

	if modelPath != "" {
		var err error
		provider, err = NewEmbedProvider(modelPath)
		if err != nil {
			fmt.Fprintf(os.Stderr, "[embed] failed: %v (using C-side fallback)\n", err)
		} else {
			C.sorokin_set_mutation_provider(C.mutation_provider_fn(C.nano_bridge_shim))
			fmt.Fprintf(os.Stderr, "[embed] mutation provider active\n")
		}
	} else {
		fmt.Fprintf(os.Stderr, "[embed] no GGUF found, using seed vocab + phonetic neighbors\n")
	}

	fmt.Println("╔══════════════════════════════════════════════════════════╗")
	fmt.Println("║  SOROKIN — Literary Necromancy Engine (Go + C)          ║")
	fmt.Println("║  Dario Equation: p(x|Φ) = softmax((B+αH+βF+γA+T)/τ)   ║")
	if provider != nil {
		fmt.Printf("║  nanollama %d dim · embedding necromancy                ║\n",
			provider.dim)
	} else {
		fmt.Println("║  1158 seed words · phonetic neighbors                   ║")
	}
	fmt.Println("╚══════════════════════════════════════════════════════════╝")

	if len(os.Args) > 1 {
		prompt := strings.Join(os.Args[1:], " ")
		cPrompt := C.CString(prompt)
		defer C.free(unsafe.Pointer(cPrompt))
		C.run_autopsy(cPrompt)
	} else {
		fmt.Println("\nEnter text for autopsy (Ctrl+D to exit):\n")
		scanner := bufio.NewScanner(os.Stdin)
		fmt.Print("> ")
		for scanner.Scan() {
			line := strings.TrimSpace(scanner.Text())
			if line == "" {
				fmt.Print("> ")
				continue
			}
			cLine := C.CString(line)
			C.run_autopsy(cLine)
			C.free(unsafe.Pointer(cLine))
			fmt.Print("> ")
		}
		fmt.Println("\n[autopsy complete]")
	}
}

