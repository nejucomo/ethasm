package main

import (
	"bufio"
	"fmt"
	"github.com/ethereum/eth-go/ethvm"
	"io"
	"os"
	"strconv"
	"strings"
)

func main() {
	os.Exit(runMain())
}

func runMain() int {
	bufout := bufio.NewWriter(os.Stdout)
	defer bufout.Flush()

	err := assemble(os.Stdin, bufout)

	if err == nil {
		return 0
	} else {
		return 1
	}
}

func assemble(source io.Reader, out io.ByteWriter) error {
	return lex(source, makeTokenAssembler(out))
}

type TokenConsumer func(line int, token string) error

func lex(source io.Reader, consume TokenConsumer) error {
	line := 0

	lscanner := bufio.NewScanner(source)
	for lscanner.Scan() {
		line += 1

		// Split off comments:
		chunk := strings.SplitN(lscanner.Text(), "//", 2)[0]

		wscanner := bufio.NewScanner(strings.NewReader(chunk))
		wscanner.Split(bufio.ScanWords)

		for wscanner.Scan() {
			token := wscanner.Text()
			err := consume(line, token)
			if err != nil {
				return err
			}
		}
	}

	return nil
}

func makeTokenAssembler(out io.ByteWriter) TokenConsumer {
	return func(line int, token string) error {
		opcode, ok := ethvm.OpCodes[token]
		if ok {
			return out.WriteByte(byte(opcode))
		}

		datum, err := strconv.ParseUint(token, 0, 64) // BUG: Handle 256 bit words, also unsigned.
		if err == nil {
			return assemblePushWord(datum, out)
		}

		return fmt.Errorf("Invalid token on line %d: %v", line, token)
	}
}

func assemblePushWord(datum uint64, out io.ByteWriter) error {
	var bytes []byte = nil

	// Build a little endian array of bytes of datum:
	for datum > 0 {
		bytes = append(bytes, byte(datum&0xff))
		datum = datum >> 8
	}

	opdelta := len(bytes)
	if opdelta > 0 {
		opdelta -= 1
	}

	opcode := byte(ethvm.PUSH1 + opdelta)

	err := out.WriteByte(opcode)
	if err != nil {
		return err
	}

	// BUG: Is the ethereum bytecode bigendian or little? This is big-endian:
	for i := len(bytes) - 1; i >= 0; i-- {
		err := out.WriteByte(bytes[i])
		if err != nil {
			return err
		}
	}

	return nil
}
