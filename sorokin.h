/* sorokin.h — CGO interface for Literary Necromancy Engine */

#ifndef SOROKIN_H
#define SOROKIN_H

#define MAX_WORD_LEN 64

/* mutation provider callback: given a word, fill results with related words */
typedef int (*mutation_provider_fn)(const char *word,
    char results[][MAX_WORD_LEN], int max_results);

/* initialize the autopsy engine (loads seed vocab, builds bigrams) */
void sorokin_init(void);

/* set external mutation provider (nanollama via Go) */
void sorokin_set_mutation_provider(mutation_provider_fn fn);

#endif /* SOROKIN_H */
