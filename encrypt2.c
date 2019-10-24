#include <string.h>
#include <openssl/conf.h>
#include <openssl/err.h>
#include <openssl/evp.h>
#include <openssl/sha.h>

void handle_errors(void);
int encrypt(unsigned char *, int, unsigned char *, unsigned char *, unsigned char *);
char * sha256(const char *, char *);

int main(int argc, char *argv[]) {
	// Set key and iv
	unsigned char *key = "11474175200000000000000000000000";
	unsigned char *iv = "0000000000000000";

	// get plaintext to be encrypted
	FILE *plainfile = fopen(argv[1], "r");
	fseek(plainfile, 0, SEEK_END);
	int fsize = ftell(plainfile);
	fseek(plainfile, 0, SEEK_SET);
	unsigned char *plaintext = malloc(fsize);
	fread(plaintext, sizeof(unsigned char), fsize, plainfile);	

	// create buffer for the ciphertext
	unsigned char *ciphertext = malloc(fsize * 2);

	// encrypt the text
	encrypt(plaintext, strlen(plaintext), key, iv, ciphertext);

	/************ SHA256 hashing **************************/
	// hash ciphertext with sha256
	unsigned char hash[32];
	SHA256(ciphertext, strlen(ciphertext), hash);
	
	// open file to hash to
	FILE *hashfile = fopen("hash2.txt", "w");
	for (int i = 0; i < 32; i++) {
		fprintf(hashfile, "%02x", hash[i]);
	}
}

void handle_errors(void) {
	ERR_print_errors_fp(stderr);
	abort();
}

int encrypt(unsigned char *plaintext, int plaintext_len, unsigned char *key,
			unsigned char *iv, unsigned char *ciphertext) {
	EVP_CIPHER_CTX *ctx;
	int len, ciphertext_len;
	
	// initialize cipher context
	ctx = EVP_CIPHER_CTX_new();
	
	EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv);
	EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len);
	ciphertext_len = len;

	EVP_EncryptFinal_ex(ctx, ciphertext + len, &len);
	
	// write the cipher to a file
	FILE *cipherfile = fopen("cipher2.out", "wb");
	fwrite(ciphertext, sizeof(unsigned char), ciphertext_len + len, cipherfile);

	EVP_CIPHER_CTX_free(ctx);
	return ciphertext_len;
}

char * sha256(const char *text, char *buffer) {
	SHA256_CTX *sha256;
	SHA256_Init(sha256);
	SHA256_Update(sha256, text, strlen(text) * sizeof(unsigned char)); // <-- might be wrong
	SHA256_Final(buffer, sha256);
	return buffer;
	return NULL;
}
