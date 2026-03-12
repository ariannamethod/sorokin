package main

// quantize.go — f16 → q4_0 GGUF quantizer
//
// Q4_0 format: blocks of 32 elements, 18 bytes each:
//   [2 bytes fp16 scale] [16 bytes: 32 x 4-bit values packed, 2 per byte]
//   Each 4-bit value ranges [0..15], representing (value - 8) * scale

import (
	"encoding/binary"
	"fmt"
	"math"
	"os"
	"sort"
	"strings"
)

// float32ToHalf converts float32 to IEEE 754 binary16
func float32ToHalf(f float32) uint16 {
	bits := math.Float32bits(f)
	sign := (bits >> 31) & 1
	exp := int((bits>>23)&0xFF) - 127
	mant := bits & 0x7FFFFF

	if exp > 15 {
		// overflow → max finite fp16
		return uint16(sign<<15 | 0x7BFF)
	}
	if exp < -14 {
		// too small → zero
		return uint16(sign << 15)
	}

	h := sign << 15
	h |= uint32(exp+15) << 10
	h |= mant >> 13
	return uint16(h)
}

// quantizeBlockQ4_0 quantizes 32 float32 values into an 18-byte Q4_0 block
func quantizeBlockQ4_0(src []float32) []byte {
	block := make([]byte, q4BytesPerBlock)

	// Find max absolute value for scale
	var amax float32
	for _, v := range src[:32] {
		a := v
		if a < 0 {
			a = -a
		}
		if a > amax {
			amax = a
		}
	}

	// Scale: maps [-8..7] → [-amax..amax*(7/8)]
	d := amax / 8.0
	id := float32(0)
	if d > 0 {
		id = 1.0 / d
	}

	// Store scale as fp16
	binary.LittleEndian.PutUint16(block[0:2], float32ToHalf(d))

	// Quantize: pack two 4-bit values per byte
	// First 16 values → low nibbles, next 16 → high nibbles (same byte)
	for j := 0; j < 16; j++ {
		v0 := src[j] * id
		v1 := src[j+16] * id

		// Round and clamp to [0..15] (stored as value+8)
		q0 := int(v0+8.5) // +8 bias, +0.5 for rounding
		q1 := int(v1+8.5)
		if q0 < 0 {
			q0 = 0
		}
		if q0 > 15 {
			q0 = 15
		}
		if q1 < 0 {
			q1 = 0
		}
		if q1 > 15 {
			q1 = 15
		}

		block[2+j] = byte(q0) | byte(q1)<<4
	}

	return block
}

// quantizeTensorToQ4_0 converts an F16 tensor to Q4_0
func quantizeTensorToQ4_0(data []byte, nel int) []byte {
	// First dequant F16 → F32
	f32 := make([]float32, nel)
	for i := 0; i < nel; i++ {
		h := binary.LittleEndian.Uint16(data[i*2 : i*2+2])
		f32[i] = half2float(h)
	}

	// Quantize F32 → Q4_0
	nblocks := nel / q4BlockSize
	out := make([]byte, nblocks*q4BytesPerBlock)
	for b := 0; b < nblocks; b++ {
		block := quantizeBlockQ4_0(f32[b*q4BlockSize : (b+1)*q4BlockSize])
		copy(out[b*q4BytesPerBlock:], block)
	}
	return out
}

// quantizeTensorF32ToQ4_0 converts an F32 tensor to Q4_0
func quantizeTensorF32ToQ4_0(data []byte, nel int) []byte {
	f32 := make([]float32, nel)
	for i := 0; i < nel; i++ {
		f32[i] = math.Float32frombits(binary.LittleEndian.Uint32(data[i*4 : i*4+4]))
	}
	nblocks := nel / q4BlockSize
	out := make([]byte, nblocks*q4BytesPerBlock)
	for b := 0; b < nblocks; b++ {
		block := quantizeBlockQ4_0(f32[b*q4BlockSize : (b+1)*q4BlockSize])
		copy(out[b*q4BytesPerBlock:], block)
	}
	return out
}

// inferGGUFType returns the gguf value type for an interface value
func inferGGUFType(v interface{}) uint32 {
	switch v.(type) {
	case uint8:
		return ggufTypeUint8
	case int8:
		return ggufTypeInt8
	case uint16:
		return ggufTypeUint16
	case int16:
		return ggufTypeInt16
	case uint32:
		return ggufTypeUint32
	case int32:
		return ggufTypeInt32
	case float32:
		return ggufTypeFloat32
	case bool:
		return ggufTypeBool
	case string:
		return ggufTypeString
	case uint64:
		return ggufTypeUint64
	case int64:
		return ggufTypeInt64
	case float64:
		return ggufTypeFloat64
	case []interface{}:
		return ggufTypeArray
	default:
		return ggufTypeUint32
	}
}

func writeGGUFString(f *os.File, s string) {
	binary.Write(f, binary.LittleEndian, uint64(len(s)))
	f.Write([]byte(s))
}

func writeGGUFValue(f *os.File, v interface{}) {
	switch val := v.(type) {
	case uint8:
		binary.Write(f, binary.LittleEndian, val)
	case int8:
		binary.Write(f, binary.LittleEndian, val)
	case uint16:
		binary.Write(f, binary.LittleEndian, val)
	case int16:
		binary.Write(f, binary.LittleEndian, val)
	case uint32:
		binary.Write(f, binary.LittleEndian, val)
	case int32:
		binary.Write(f, binary.LittleEndian, val)
	case float32:
		binary.Write(f, binary.LittleEndian, val)
	case bool:
		if val {
			binary.Write(f, binary.LittleEndian, uint8(1))
		} else {
			binary.Write(f, binary.LittleEndian, uint8(0))
		}
	case string:
		writeGGUFString(f, val)
	case uint64:
		binary.Write(f, binary.LittleEndian, val)
	case int64:
		binary.Write(f, binary.LittleEndian, val)
	case float64:
		binary.Write(f, binary.LittleEndian, val)
	case []interface{}:
		if len(val) == 0 {
			binary.Write(f, binary.LittleEndian, uint32(ggufTypeUint32))
			binary.Write(f, binary.LittleEndian, uint64(0))
			return
		}
		elemType := inferGGUFType(val[0])
		binary.Write(f, binary.LittleEndian, elemType)
		binary.Write(f, binary.LittleEndian, uint64(len(val)))
		for _, elem := range val {
			writeGGUFValue(f, elem)
		}
	}
}

// QuantizeGGUF reads a source GGUF, quantizes weight tensors to Q4_0, writes output
func QuantizeGGUF(srcPath, dstPath string) error {
	// Load source
	src, err := LoadGGUF(srcPath)
	if err != nil {
		return fmt.Errorf("load source: %w", err)
	}

	// Decide which tensors to quantize
	// Quantize: embedding, attention, MLP projections, output
	// Keep F32: norm weights (small, need precision)
	type tensorEntry struct {
		name string
		info *GGUFTensorInfo
	}
	var tensorList []tensorEntry
	for name, info := range src.Tensors {
		tensorList = append(tensorList, tensorEntry{name, info})
	}
	sort.Slice(tensorList, func(i, j int) bool {
		return tensorList[i].info.Offset < tensorList[j].info.Offset
	})

	// Prepare output tensors
	type outTensor struct {
		name    string
		info    GGUFTensorInfo // copy with updated type
		data    []byte
	}
	var outTensors []outTensor
	var totalSaved int64

	for _, te := range tensorList {
		name := te.name
		info := te.info
		srcData, _, err := src.GetTensor(name)
		if err != nil {
			return fmt.Errorf("get tensor %s: %w", name, err)
		}

		nel := uint64(1)
		for d := uint32(0); d < info.NDims; d++ {
			nel *= info.Dims[d]
		}

		isNorm := strings.Contains(name, "norm")
		shouldQuantize := !isNorm && (info.Type == ggmlTypeF16 || info.Type == ggmlTypeF32) && nel%q4BlockSize == 0

		newInfo := *info
		var newData []byte

		if shouldQuantize {
			switch info.Type {
			case ggmlTypeF16:
				newData = quantizeTensorToQ4_0(srcData, int(nel))
			case ggmlTypeF32:
				newData = quantizeTensorF32ToQ4_0(srcData, int(nel))
			}
			newInfo.Type = ggmlTypeQ4_0
			saved := int64(len(srcData)) - int64(len(newData))
			totalSaved += saved
			fmt.Printf("  %-45s %s → q4_0  %6.2f MB → %6.2f MB\n",
				name, typeName(info.Type),
				float64(len(srcData))/1024/1024,
				float64(len(newData))/1024/1024)
		} else {
			newData = srcData
			fmt.Printf("  %-45s %s (keep)\n", name, typeName(info.Type))
		}

		outTensors = append(outTensors, outTensor{name, newInfo, newData})
	}

	fmt.Printf("\n  Total saved: %.2f MB\n", float64(totalSaved)/1024/1024)

	// Write output GGUF
	f, err := os.Create(dstPath)
	if err != nil {
		return fmt.Errorf("create output: %w", err)
	}
	defer f.Close()

	// Header
	binary.Write(f, binary.LittleEndian, uint32(ggufMagic))
	binary.Write(f, binary.LittleEndian, uint32(ggufVersion))
	binary.Write(f, binary.LittleEndian, uint64(len(outTensors)))
	binary.Write(f, binary.LittleEndian, uint64(len(src.Meta.KV)))

	// Metadata KV (copied from source, preserving types)
	// Sort keys for deterministic output
	var keys []string
	for k := range src.Meta.KV {
		keys = append(keys, k)
	}
	sort.Strings(keys)

	for _, key := range keys {
		val := src.Meta.KV[key]
		writeGGUFString(f, key)
		vtype := inferGGUFType(val)
		binary.Write(f, binary.LittleEndian, vtype)
		writeGGUFValue(f, val)
	}

	// Tensor info — compute offsets
	// First pass: calculate offsets within data blob
	var dataOffset uint64
	for i := range outTensors {
		outTensors[i].info.Offset = dataOffset
		size := uint64(len(outTensors[i].data))
		dataOffset += size
		// Align each tensor to 32 bytes
		if pad := dataOffset % 32; pad != 0 {
			dataOffset += 32 - pad
		}
	}

	// Write tensor info
	for _, t := range outTensors {
		writeGGUFString(f, t.name)
		binary.Write(f, binary.LittleEndian, t.info.NDims)
		for d := uint32(0); d < t.info.NDims; d++ {
			binary.Write(f, binary.LittleEndian, t.info.Dims[d])
		}
		binary.Write(f, binary.LittleEndian, t.info.Type)
		binary.Write(f, binary.LittleEndian, t.info.Offset)
	}

	// Alignment padding (32 bytes)
	pos, _ := f.Seek(0, 1)
	if pad := pos % 32; pad != 0 {
		zeros := make([]byte, 32-pad)
		f.Write(zeros)
	}

	// Tensor data
	for _, t := range outTensors {
		f.Write(t.data)
		// Align to 32
		if pad := len(t.data) % 32; pad != 0 {
			zeros := make([]byte, 32-pad)
			f.Write(zeros)
		}
	}

	return nil
}

func typeName(t uint32) string {
	switch t {
	case ggmlTypeF32:
		return "f32"
	case ggmlTypeF16:
		return "f16"
	case ggmlTypeQ4_0:
		return "q4_0"
	case ggmlTypeQ8_0:
		return "q8_0"
	case ggmlTypeQ4_K:
		return "q4_k"
	case ggmlTypeQ6_K:
		return "q6_k"
	default:
		return fmt.Sprintf("type_%d", t)
	}
}
