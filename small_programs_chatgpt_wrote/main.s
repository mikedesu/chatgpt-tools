	.file	"main2.c"
	.text
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC1:
	.string	"Cube Renderer"
	.section	.text.startup,"ax",@progbits
	.globl	main
	.type	main, @function
main:
.LFB5536:
	.cfi_startproc
	endbr64
	pushq	%r15
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
	movl	$72, %edi
	movabsq	$4539628425446424576, %rdx
	movabsq	$4539628427593908224, %rsi
	movabsq	$-4683743611408351232, %rcx
	pushq	%r14
	.cfi_def_cfa_offset 24
	.cfi_offset 14, -24
	xorl	%r14d, %r14d
	pushq	%r13
	.cfi_def_cfa_offset 32
	.cfi_offset 13, -32
	pushq	%r12
	.cfi_def_cfa_offset 40
	.cfi_offset 12, -40
	pushq	%rbp
	.cfi_def_cfa_offset 48
	.cfi_offset 6, -48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	.cfi_offset 3, -56
	subq	$184, %rsp
	.cfi_def_cfa_offset 240
	movq	%fs:40, %rax
	movq	%rax, 168(%rsp)
	movabsq	$-4683743609260867584, %rax
	movq	%rdx, 80(%rsp)
	movq	%rsi, 88(%rsp)
	movq	%rdx, 96(%rsp)
	movq	%rdx, 112(%rsp)
	movq	%rsi, 128(%rsp)
	movq	%rdx, 144(%rsp)
	movq	%rcx, 104(%rsp)
	movq	%rcx, 160(%rsp)
	movq	%rax, 72(%rsp)
	movq	%rax, 120(%rsp)
	movq	%rax, 136(%rsp)
	movq	%rax, 152(%rsp)
	call	malloc@PLT
	movl	$72, %ecx
	movq	%rax, %rbp
	movb	$1, %al
	movq	%rbp, %rdi
	rep stosb
	movl	$32, %edi
	movw	$0, 0(%rbp)
	movabsq	$1116708602117, %rax
	movq	%rax, 40(%rbp)
	movabsq	$72621669289951493, %rax
	movq	%rax, 50(%rbp)
	movabsq	$1112413438210, %rax
	movq	%rax, 4(%rbp)
	movabsq	$73747569196728580, %rax
	movq	%rax, 12(%rbp)
	movabsq	$72621656405049607, %rax
	movq	%rax, 20(%rbp)
	movabsq	$72903148561629446, %rax
	movq	%rax, 28(%rbp)
	movabsq	$1112413765895, %rax
	movw	$0, 36(%rbp)
	movl	$17039360, 60(%rbp)
	movq	%rax, 64(%rbp)
	call	SDL_Init@PLT
	movl	$6, %r9d
	movl	$600, %r8d
	movl	$800, %ecx
	movl	$805240832, %edx
	movl	$805240832, %esi
	leaq	.LC1(%rip), %rdi
	call	SDL_CreateWindow@PLT
	movq	%rax, %rdi
	movq	%rax, %r12
	call	SDL_GL_CreateContext@PLT
	xorps	%xmm2, %xmm2
	movss	.LC2(%rip), %xmm3
	movaps	%xmm2, %xmm1
	movaps	%xmm2, %xmm0
	movq	%rax, %r13
	call	glClearColor@PLT
	movl	$5889, %edi
	call	glMatrixMode@PLT
	call	glLoadIdentity@PLT
	movsd	.LC3(%rip), %xmm3
	movb	$4, %al
	movsd	.LC4(%rip), %xmm2
	movsd	.LC5(%rip), %xmm1
	movsd	.LC6(%rip), %xmm0
	call	gluPerspective@PLT
	movl	$5888, %edi
	call	glMatrixMode@PLT
	call	glLoadIdentity@PLT
	xorps	%xmm1, %xmm1
	movss	.LC7(%rip), %xmm2
	movaps	%xmm1, %xmm0
	call	glTranslatef@PLT
	movl	$7425, %edi
	call	glShadeModel@PLT
	movl	$2929, %edi
	call	glEnable@PLT
	movl	$515, %edi
	call	glDepthFunc@PLT
	movl	$32884, %edi
	call	glEnableClientState@PLT
	movl	$0x00000000, 12(%rsp)
.L2:
	movl	$1, %ebx
	leaq	16(%rsp), %r15
.L6:
	movq	%r15, %rdi
	call	SDL_PollEvent@PLT
	testl	%eax, %eax
	je	.L10
	cmpl	$256, 16(%rsp)
	cmove	%r14d, %ebx
	jmp	.L6
.L10:
	movl	$16640, %edi
	call	glClear@PLT
	call	glLoadIdentity@PLT
	xorps	%xmm1, %xmm1
	movss	.LC7(%rip), %xmm2
	movaps	%xmm1, %xmm0
	call	glTranslatef@PLT
	movss	.LC2(%rip), %xmm2
	movss	12(%rsp), %xmm0
	xorps	%xmm3, %xmm3
	movaps	%xmm2, %xmm1
	call	glRotatef@PLT
	movss	.LC2(%rip), %xmm2
	movaps	%xmm2, %xmm1
	movaps	%xmm2, %xmm0
	call	glColor3f@PLT
	leaq	72(%rsp), %rcx
	xorl	%edx, %edx
	movl	$5126, %esi
	movl	$3, %edi
	call	glVertexPointer@PLT
	movq	%rbp, %rcx
	movl	$5123, %edx
	movl	$36, %esi
	movl	$4, %edi
	call	glDrawElements@PLT
	movq	%r12, %rdi
	call	SDL_GL_SwapWindow@PLT
	movss	12(%rsp), %xmm4
	addss	.LC8(%rip), %xmm4
	movss	%xmm4, 12(%rsp)
	testl	%ebx, %ebx
	jne	.L2
	movl	$32884, %edi
	call	glDisableClientState@PLT
	movq	%r13, %rdi
	call	SDL_GL_DeleteContext@PLT
	movq	%r12, %rdi
	call	SDL_DestroyWindow@PLT
	call	SDL_Quit@PLT
	movq	168(%rsp), %rax
	subq	%fs:40, %rax
	je	.L7
	call	__stack_chk_fail@PLT
.L7:
	addq	$184, %rsp
	.cfi_def_cfa_offset 56
	xorl	%eax, %eax
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%rbp
	.cfi_def_cfa_offset 40
	popq	%r12
	.cfi_def_cfa_offset 32
	popq	%r13
	.cfi_def_cfa_offset 24
	popq	%r14
	.cfi_def_cfa_offset 16
	popq	%r15
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE5536:
	.size	main, .-main
	.section	.rodata.cst4,"aM",@progbits,4
	.align 4
.LC2:
	.long	1065353216
	.section	.rodata.cst8,"aM",@progbits,8
	.align 8
.LC3:
	.long	0
	.long	1079574528
	.align 8
.LC4:
	.long	-1610612736
	.long	1069128089
	.align 8
.LC5:
	.long	1610612736
	.long	1073042773
	.align 8
.LC6:
	.long	0
	.long	1078362112
	.section	.rodata.cst4
	.align 4
.LC7:
	.long	-1046478848
	.align 4
.LC8:
	.long	1056964608
	.ident	"GCC: (Ubuntu 11.3.0-1ubuntu1~22.04) 11.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:
