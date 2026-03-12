package main

// engine.go — nanollama inference engine for sorokin
// Extracted from nanollama main.go (Engine, GenParams, sampling)

import (
	"math"
	"math/rand"
	"time"
)

// GenParams controls text generation
type GenParams struct {
	MaxTokens   int
	Temperature float32
	TopP        float32
	TopK        int
}

// Engine wraps model + tokenizer for generation
type Engine struct {
	model      *LlamaModel
	tokenizer  *Tokenizer
	rng        *rand.Rand
	repPenalty float32
	repWindow  int
}

// NewEngine creates an Engine from a loaded model
func NewEngine(model *LlamaModel, tokenizer *Tokenizer) *Engine {
	return &Engine{
		model:      model,
		tokenizer:  tokenizer,
		rng:        rand.New(rand.NewSource(time.Now().UnixNano())),
		repPenalty: 1.15,
		repWindow:  64,
	}
}

// GenerateQuiet produces text without streaming to stdout
func (e *Engine) GenerateQuiet(prompt string, p GenParams) string {
	tokens := e.tokenizer.Encode(prompt, true)
	e.model.Reset()

	pos := 0
	for _, tok := range tokens {
		e.model.Forward(tok, pos)
		pos++
		if pos >= e.model.Config.SeqLen-1 {
			break
		}
	}

	var output []byte
	recentTokens := make([]int, 0, e.repWindow)

	for i := 0; i < p.MaxTokens && len(output) < 8192; i++ {
		logits := e.model.State.Logits

		if e.repPenalty > 1.0 && len(recentTokens) > 0 {
			for _, tok := range recentTokens {
				if tok >= 0 && tok < e.model.Config.VocabSize {
					if logits[tok] > 0 {
						logits[tok] /= e.repPenalty
					} else {
						logits[tok] *= e.repPenalty
					}
				}
			}
		}

		var next int
		if p.TopP < 1.0 {
			next = e.sampleTopP(p.Temperature, p.TopP)
		} else {
			next = e.sampleTopK(p.Temperature, p.TopK)
		}

		recentTokens = append(recentTokens, next)
		if len(recentTokens) > e.repWindow {
			recentTokens = recentTokens[1:]
		}

		if next == e.tokenizer.EosID {
			break
		}

		piece := e.tokenizer.DecodeToken(next)
		output = append(output, []byte(piece)...)

		e.model.Forward(next, pos)
		pos++
		if pos >= e.model.Config.SeqLen {
			break
		}
	}

	return string(output)
}

// sampleTopK samples from top-k logits
func (e *Engine) sampleTopK(temp float32, topK int) int {
	logits := e.model.State.Logits
	vocab := e.model.Config.VocabSize

	if temp <= 0 {
		return argmax(logits, vocab)
	}
	if topK > vocab {
		topK = vocab
	}

	type idxVal struct {
		idx int
		val float32
	}
	top := make([]idxVal, topK)
	for i := 0; i < topK; i++ {
		top[i] = idxVal{-1, -1e30}
	}

	for i := 0; i < vocab; i++ {
		if logits[i] > top[topK-1].val {
			top[topK-1] = idxVal{i, logits[i]}
			for j := topK - 1; j > 0 && top[j].val > top[j-1].val; j-- {
				top[j], top[j-1] = top[j-1], top[j]
			}
		}
	}

	maxVal := top[0].val
	probs := make([]float32, topK)
	var sum float32
	for i := 0; i < topK; i++ {
		if top[i].idx < 0 {
			break
		}
		probs[i] = float32(math.Exp(float64((top[i].val - maxVal) / temp)))
		sum += probs[i]
	}

	r := e.rng.Float32() * sum
	var cdf float32
	for i := 0; i < topK; i++ {
		cdf += probs[i]
		if r <= cdf {
			return top[i].idx
		}
	}
	return top[0].idx
}

// sampleTopP samples using nucleus (top-p) sampling
func (e *Engine) sampleTopP(temp, topP float32) int {
	logits := e.model.State.Logits
	vocab := e.model.Config.VocabSize

	if temp <= 0 {
		return argmax(logits, vocab)
	}

	maxVal := logits[0]
	for i := 1; i < vocab; i++ {
		if logits[i] > maxVal {
			maxVal = logits[i]
		}
	}

	type idxProb struct {
		idx  int
		prob float32
	}
	candidates := make([]idxProb, vocab)
	var sum float32
	for i := 0; i < vocab; i++ {
		p := float32(math.Exp(float64((logits[i] - maxVal) / temp)))
		candidates[i] = idxProb{i, p}
		sum += p
	}

	invSum := float32(1.0) / sum
	for i := range candidates {
		candidates[i].prob *= invSum
	}

	// Simple sort by prob descending
	for i := 0; i < len(candidates)-1; i++ {
		for j := i + 1; j < len(candidates); j++ {
			if candidates[j].prob > candidates[i].prob {
				candidates[i], candidates[j] = candidates[j], candidates[i]
			}
		}
	}

	var cumsum float32
	for i := range candidates {
		cumsum += candidates[i].prob
		if cumsum >= topP {
			r := e.rng.Float32() * cumsum
			var cdf2 float32
			for j := 0; j <= i; j++ {
				cdf2 += candidates[j].prob
				if r <= cdf2 {
					return candidates[j].idx
				}
			}
			return candidates[0].idx
		}
	}
	return candidates[0].idx
}

func argmax(logits []float32, n int) int {
	best := 0
	for i := 1; i < n; i++ {
		if logits[i] > logits[best] {
			best = i
		}
	}
	return best
}

func estimateParams(m *LlamaModel) int {
	cfg := &m.Config
	embed := cfg.VocabSize * cfg.EmbedDim
	output := cfg.VocabSize * cfg.EmbedDim
	attnPerLayer := cfg.EmbedDim*(cfg.NumHeads*cfg.HeadDim) +
		cfg.EmbedDim*(cfg.NumKVHeads*cfg.HeadDim) +
		cfg.EmbedDim*(cfg.NumKVHeads*cfg.HeadDim) +
		cfg.EmbedDim*cfg.EmbedDim
	mlpPerLayer := cfg.EmbedDim*cfg.IntermSize*2 +
		cfg.IntermSize*cfg.EmbedDim
	normsPerLayer := cfg.EmbedDim * 2
	perLayer := attnPerLayer + mlpPerLayer + normsPerLayer
	return embed + output + cfg.NumLayers*perLayer + cfg.EmbedDim
}
