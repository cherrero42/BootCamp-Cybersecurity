/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   corsair.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/05/06 14:27:53 by cherrero          #+#    #+#             */
/*   Updated: 2023/05/30 21:25:45 by cherrero         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */


#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <openssl/rsa.h>
#include <openssl/bn.h>
#include <openssl/pem.h>

int 	BUFFER_SIZE = 1024;
char	s1[1000];
char	sout[1000];
int		fd;
int		len;
RSA		*rsa1;
RSA		*rsa2;
RSA		*private;
BIO		*fp1;
BIO		*fp2;
const BIGNUM	*n1;
const BIGNUM	*n2;
const BIGNUM	*e;
BIGNUM			*d;
BN_CTX			*ctx;
BIGNUM			*gcd;
BIGNUM			*q1;
BIGNUM			*q2;
BIGNUM			*phi;
BIGNUM			*phi1;
BIGNUM			*phi2;
	
void	ft_leaks(void)
{
	system("leaks -q corsair");
}

int main(int argc, char **argv)
{
	atexit(ft_leaks);
	if (argc != 4)
    {
		printf("Usage args: 2 public certificates (.pem) & 1 encrypted file (.bin)");
        return (0);
    }

	fp1 = BIO_new_file(argv[1], "r");
	fp2 = BIO_new_file(argv[2], "r");
	q1 = BN_new();
	q2 = BN_new();
	gcd = BN_new();
	ctx = BN_CTX_new();
	phi = BN_new();
	phi1 = BN_new();
	phi2 = BN_new();
	d = BN_new();
	private = RSA_new();
	
	rsa1 = PEM_read_bio_RSA_PUBKEY(fp1, NULL, NULL, NULL);
	rsa2 = PEM_read_bio_RSA_PUBKEY(fp2, NULL, NULL, NULL);
	if (!rsa1 || !rsa2)
	{
		printf("Read error\n");
		exit(0);
	}
	printf("\nPublic 1:");
	printf(argv[1]);
	RSA_print_fp(stdout, rsa1, 0);
	printf("\nPublic 2:");
	printf(argv[3]);
	printf("\n");
	RSA_print_fp(stdout, rsa2, 0);
	RSA_get0_key(rsa1, &n1, &e, NULL);
	RSA_get0_key(rsa2, &n2, NULL, NULL);
	printf("\nPrime common: ");
	BN_gcd(gcd, n1, n2, ctx);
	BN_print_fp(stdout, gcd);
	
	if (BN_is_one(gcd))
	{
		printf("\n\x1b[31mThese public keys do not have a common prime other than 1.\x1b[0m\n");
		BN_free(gcd);
		BN_free(q1);
		BN_free(q2);
	}
	else
	{
		BN_div(q1, NULL, n1, gcd, ctx);
		BN_div(q2, NULL, n2, gcd, ctx);
		BN_sub(phi1, q1, BN_value_one());
		BN_sub(phi2, gcd, BN_value_one());
		BN_mul(phi, phi1, phi2, ctx);
		BN_mod_inverse(d, e, phi, ctx);
		RSA_set0_key(private, BN_dup(n1),
		BN_dup(e), BN_dup(d));
		printf("\nPrivate key extracted:\n");
		RSA_print_fp(stdout, private, 0);
		RSA_set0_factors(rsa1, gcd, q1);
		RSA_set0_factors(rsa2, gcd, q2);
	

		fd = open(argv[3], O_RDONLY);
		if (!fd)
			exit(1);
		if (fd < 0)
		{
			printf("Can't read encrypted file\n");
			exit(0);
		}
		len = read(fd, s1, BUFFER_SIZE);
		printf("Decrypting...\n");
		if (RSA_private_decrypt(RSA_size(private), s1, sout, private, RSA_PKCS1_PADDING) < 0)
		{
			printf("I can't decrypt the file\n");
			exit(0);
		}
		printf("\x1b[32mFile successfully decrypted: \n%s\x1b[0m\n", sout);
		close(fd);
		}
	BIO_free(fp1);
	BIO_free(fp2);
	RSA_free(rsa1);
	RSA_free(rsa2);
	RSA_free(private);
	BN_CTX_free(ctx);
	BN_free(phi);
	BN_free(phi1);
	BN_free(phi2);
	BN_free(d);
	}
