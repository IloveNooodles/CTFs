	.file "main.pas"
// Begin asmlist al_procedures

.section .text.n_p$foreign_$$_run$ansistring
	.balign 8
.globl	P$FOREIGN_$$_RUN$ANSISTRING
	.type	P$FOREIGN_$$_RUN$ANSISTRING,@function
P$FOREIGN_$$_RUN$ANSISTRING:
	stp	x29,x30,[sp, #-16]!
	mov	x29,sp
	movz	x16,#8256
	sub	sp,sp,x16
	str	x0,[sp]
	ldr	x0,[sp]
	bl	fpc_ansistr_incr_ref
	movz	x0,#8048
	add	x2,sp,x0
	movz	x0,#8072
	add	x1,sp,x0
	movz	w0,#1
	bl	fpc_pushexceptaddr
	bl	fpc_setjmp
	ubfiz	x1,x0,#0,#32
	sxtw	x0,w1
	str	x0,[sp, #8240]
	cmp	w1,#0
	b.ne	.Lj6
	add	x0,sp,#16
	movz	x1,#1024
	bl	SYSTEM_$$_GETMEM$POINTER$QWORD
	ldr	x0,[sp, #16]
	str	x0,[sp, #8]
	ldr	x0,[sp, #8]
	movz	w2,#0
	movz	x1,#1024
	bl	SYSTEM_$$_FILLBYTE$formal$INT64$BYTE
	movn	w0,#0
	strh	w0,[sp, #8040]
	ldr	x0,[sp]
	str	x0,[sp, #24]
	ldr	x0,[sp]
	ldr	x1,[sp]
	cmp	x1,#0
	b.eq	.Lj7
	ldur	x1,[x1, #-8]
.Lj7:
	sub	x0,x0,#1
	add	x0,x0,x1
	str	x0,[sp, #32]
	ldr	x0,[sp, #24]
	cmp	x0,#0
	b.eq	.Lj8
	b	.Lj9
.Lj8:
	b	.Lj6
.Lj9:
	.balign 4
.Lj10:
	ldr	x0,[sp, #24]
	ldrb	w0,[x0]
	cmp	w0,#101
	b.lo	.Lj14
	mov	w1,w0
	sub	w0,w0,#101
	cmp	w1,#101
	b.eq	.Lj18
	mov	w1,w0
	sub	w0,w0,#1
	cmp	w1,#1
	b.eq	.Lj15
	mov	w1,w0
	sub	w0,w0,#1
	cmp	w1,#1
	b.eq	.Lj20
	mov	w1,w0
	sub	w0,w0,#2
	cmp	w1,#2
	b.eq	.Lj19
	mov	w1,w0
	sub	w0,w0,#5
	cmp	w1,#5
	b.eq	.Lj21
	mov	w1,w0
	sub	w0,w0,#1
	cmp	w1,#1
	b.eq	.Lj16
	mov	w1,w0
	sub	w0,w0,#3
	cmp	w1,#3
	b.eq	.Lj17
	b	.Lj14
.Lj15:
	ldr	x0,[sp, #8]
	sub	x0,x0,#1
	str	x0,[sp, #8]
	b	.Lj13
.Lj16:
	ldr	x0,[sp, #8]
	add	x0,x0,#1
	str	x0,[sp, #8]
	b	.Lj13
.Lj17:
	ldr	x0,[sp, #8]
	ldrb	w1,[x0]
	add	w1,w1,#1
	uxtb	w1,w1
	strb	w1,[x0]
	b	.Lj13
.Lj18:
	ldr	x1,[sp, #8]
	ldrb	w0,[x1]
	sub	w0,w0,#1
	uxtb	w0,w0
	strb	w0,[x1]
	b	.Lj13
.Lj19:
	adrp	x0,:got:FPC_THREADVAR_RELOCATE
	ldr	x0,[x0, :got_lo12:FPC_THREADVAR_RELOCATE]
	ldur	x1,[x0]
	cmp	x1,#0
	b.eq	.Lj22
	adrp	x2,:got:U_$SYSTEM_$$_STDOUT
	ldr	x2,[x2, :got_lo12:U_$SYSTEM_$$_STDOUT]
	ldur	w0,[x2]
	blr	x1
	mov	x1,x0
	b	.Lj23
.Lj22:
	adrp	x1,:got:U_$SYSTEM_$$_STDOUT
	ldr	x1,[x1, :got_lo12:U_$SYSTEM_$$_STDOUT]
	add	x1,x1,#8
.Lj23:
	ldr	x0,[sp, #8]
	ldrb	w2,[x0]
	movz	w0,#0
	bl	fpc_write_text_char
	bl	fpc_iocheck
	adrp	x0,:got:FPC_THREADVAR_RELOCATE
	ldr	x0,[x0, :got_lo12:FPC_THREADVAR_RELOCATE]
	ldur	x2,[x0]
	cmp	x2,#0
	b.eq	.Lj24
	adrp	x1,:got:U_$SYSTEM_$$_STDOUT
	ldr	x1,[x1, :got_lo12:U_$SYSTEM_$$_STDOUT]
	ldur	w0,[x1]
	blr	x2
	b	.Lj25
.Lj24:
	adrp	x0,:got:U_$SYSTEM_$$_STDOUT
	ldr	x0,[x0, :got_lo12:U_$SYSTEM_$$_STDOUT]
	add	x0,x0,#8
.Lj25:
	bl	fpc_write_end
	bl	fpc_iocheck
	b	.Lj13
.Lj20:
	ldr	x0,[sp, #8]
	ldrb	w0,[x0]
	cmp	w0,#0
	b.eq	.Lj26
	b	.Lj27
.Lj26:
	movz	w0,#1
	strh	w0,[sp, #8044]
	b	.Lj29
	.balign 4
.Lj28:
	ldr	x0,[sp, #24]
	add	x0,x0,#1
	str	x0,[sp, #24]
	ldr	x0,[sp, #24]
	ldrb	w0,[x0]
	cmp	w0,#0
	b.eq	.Lj35
	mov	w1,w0
	sub	w0,w0,#103
	cmp	w1,#103
	b.eq	.Lj33
	mov	w1,w0
	sub	w0,w0,#7
	cmp	w1,#7
	b.eq	.Lj34
	b	.Lj32
.Lj33:
	ldrh	w0,[sp, #8044]
	add	w0,w0,#1
	uxth	w0,w0
	strh	w0,[sp, #8044]
	b	.Lj31
.Lj34:
	ldrh	w0,[sp, #8044]
	sub	w0,w0,#1
	uxth	w0,w0
	strh	w0,[sp, #8044]
	b	.Lj31
.Lj35:
	movz	w0,#0
	bl	SYSTEM_$$_HALT$LONGINT
	b	.Lj31
.Lj32:
.Lj31:
.Lj29:
	ldrh	w0,[sp, #8044]
	cmp	w0,#0
	b.hi	.Lj36
	b	.Lj37
.Lj36:
	ldr	x1,[sp, #24]
	ldr	x0,[sp, #32]
	cmp	x1,x0
	b.ls	.Lj38
	b	.Lj37
.Lj38:
	b	.Lj28
.Lj37:
	b	.Lj30
.Lj30:
	b	.Lj39
.Lj27:
	ldrsh	w0,[sp, #8040]
	add	w0,w0,#1
	sxth	w0,w0
	strh	w0,[sp, #8040]
	ldrh	w0,[sp, #8040]
	ldr	x1,[sp, #24]
	add	x0,sp,x0,lsl #3
	stur	x1,[x0, #40]
.Lj39:
	b	.Lj13
.Lj21:
	ldr	x0,[sp, #8]
	ldrb	w0,[x0]
	cmp	w0,#0
	b.hi	.Lj40
	b	.Lj41
.Lj40:
	ldrh	w0,[sp, #8040]
	add	x0,sp,x0,lsl #3
	ldur	x0,[x0, #40]
	str	x0,[sp, #24]
	b	.Lj42
.Lj41:
	ldrsh	w0,[sp, #8040]
	sub	w0,w0,#1
	sxth	w0,w0
	strh	w0,[sp, #8040]
.Lj42:
	b	.Lj13
.Lj14:
.Lj13:
	ldr	x0,[sp, #24]
	add	x0,x0,#1
	str	x0,[sp, #24]
	ldr	x0,[sp, #24]
	ldr	x1,[sp, #32]
	cmp	x0,x1
	b.hi	.Lj12
	b	.Lj10
.Lj12:
	ldr	x0,[sp, #16]
	movz	x1,#1024
	bl	SYSTEM_$$_FREEMEM$POINTER$QWORD
.Lj6:
	bl	fpc_popaddrstack
	mov	x0,sp
	bl	fpc_ansistr_decr_ref
	ldr	x0,[sp, #8240]
	cmp	x0,#0
	b.eq	.Lj5
	bl	fpc_reraise
.Lj5:
	mov	sp,x29
	ldp	x29,x30,[sp], #16
	ret
.Le0:
	.size	P$FOREIGN_$$_RUN$ANSISTRING, .Le0 - P$FOREIGN_$$_RUN$ANSISTRING

.section .text.n_main
	.balign 8
.globl	PASCALMAIN
	.type	PASCALMAIN,@function
PASCALMAIN:
.globl	main
	.type	main,@function
main:
	stp	x29,x30,[sp, #-16]!
	mov	x29,sp
	bl	fpc_initializeunits
	adrp	x0,TC_$P$FOREIGN_$$_CODE
	add	x0,x0,:lo12:TC_$P$FOREIGN_$$_CODE
	ldur	x0,[x0]
	bl	P$FOREIGN_$$_RUN$ANSISTRING
	bl	fpc_do_exit
	ldp	x29,x30,[sp], #16
	ret
.Le1:
	.size	main, .Le1 - main

.section .text.n_p$foreign_$$_init_implicit$
	.balign 8
.globl	INIT$_$P$FOREIGN
	.type	INIT$_$P$FOREIGN,@function
INIT$_$P$FOREIGN:
.globl	P$FOREIGN_$$_init_implicit$
	.type	P$FOREIGN_$$_init_implicit$,@function
P$FOREIGN_$$_init_implicit$:
	stp	x29,x30,[sp, #-16]!
	mov	x29,sp
	ldp	x29,x30,[sp], #16
	ret
.Le2:
	.size	P$FOREIGN_$$_init_implicit$, .Le2 - P$FOREIGN_$$_init_implicit$

.section .text.n_p$foreign_$$_finalize_implicit$
	.balign 8
.globl	PASCALFINALIZE
	.type	PASCALFINALIZE,@function
PASCALFINALIZE:
.globl	FINALIZE$_$P$FOREIGN
	.type	FINALIZE$_$P$FOREIGN,@function
FINALIZE$_$P$FOREIGN:
.globl	P$FOREIGN_$$_finalize_implicit$
	.type	P$FOREIGN_$$_finalize_implicit$,@function
P$FOREIGN_$$_finalize_implicit$:
	stp	x29,x30,[sp, #-16]!
	mov	x29,sp
	adrp	x0,TC_$P$FOREIGN_$$_CODE
	add	x0,x0,:lo12:TC_$P$FOREIGN_$$_CODE
	bl	fpc_ansistr_decr_ref
	ldp	x29,x30,[sp], #16
	ret
.Le3:
	.size	P$FOREIGN_$$_finalize_implicit$, .Le3 - P$FOREIGN_$$_finalize_implicit$

.section .text
// End asmlist al_procedures
// Begin asmlist al_globals

.section .data.n_INITFINAL
	.balign 8
.globl	INITFINAL
	.type	INITFINAL,@object
INITFINAL:
	.quad	2,0
	.quad	INIT$_$SYSTEM
	.quad	0
	.quad	INIT$_$P$FOREIGN
	.quad	FINALIZE$_$P$FOREIGN
.Le4:
	.size	INITFINAL, .Le4 - INITFINAL

.section .data.n_FPC_THREADVARTABLES
	.balign 8
.globl	FPC_THREADVARTABLES
	.type	FPC_THREADVARTABLES,@object
FPC_THREADVARTABLES:
	.long	1
	.quad	THREADVARLIST_$SYSTEM$indirect
.Le5:
	.size	FPC_THREADVARTABLES, .Le5 - FPC_THREADVARTABLES

.section .data.n_FPC_RESOURCESTRINGTABLES
	.balign 8
.globl	FPC_RESOURCESTRINGTABLES
	.type	FPC_RESOURCESTRINGTABLES,@object
FPC_RESOURCESTRINGTABLES:
	.quad	0
.Le6:
	.size	FPC_RESOURCESTRINGTABLES, .Le6 - FPC_RESOURCESTRINGTABLES

.section .data.n_FPC_WIDEINITTABLES
	.balign 8
.globl	FPC_WIDEINITTABLES
	.type	FPC_WIDEINITTABLES,@object
FPC_WIDEINITTABLES:
	.quad	0
.Le7:
	.size	FPC_WIDEINITTABLES, .Le7 - FPC_WIDEINITTABLES

.section .data.n_FPC_RESSTRINITTABLES
	.balign 8
.globl	FPC_RESSTRINITTABLES
	.type	FPC_RESSTRINITTABLES,@object
FPC_RESSTRINITTABLES:
	.quad	0
.Le8:
	.size	FPC_RESSTRINITTABLES, .Le8 - FPC_RESSTRINITTABLES

.section .fpc.n_version
	.balign 16
	.type	__fpc_ident,@object
__fpc_ident:
	.ascii	"FPC 3.2.2+dfsg-9ubuntu1 [2022/04/11] for aarch64 - "
	.ascii	"Linux"
.Le9:
	.size	__fpc_ident, .Le9 - __fpc_ident

.section .data.n___stklen
	.balign 8
.globl	__stklen
	.type	__stklen,@object
__stklen:
	.quad	8388608
.Le10:
	.size	__stklen, .Le10 - __stklen

.section .data.n___heapsize
	.balign 8
.globl	__heapsize
	.type	__heapsize,@object
__heapsize:
	.quad	0
.Le11:
	.size	__heapsize, .Le11 - __heapsize

.section .data.n___fpc_valgrind
	.balign 8
.globl	__fpc_valgrind
	.type	__fpc_valgrind,@object
__fpc_valgrind:
	.byte	0
.Le12:
	.size	__fpc_valgrind, .Le12 - __fpc_valgrind

.section .data.n_FPC_RESLOCATION
	.balign 8
.globl	FPC_RESLOCATION
	.type	FPC_RESLOCATION,@object
FPC_RESLOCATION:
	.quad	0
.Le13:
	.size	FPC_RESLOCATION, .Le13 - FPC_RESLOCATION
// End asmlist al_globals
// Begin asmlist al_const

.section .rodata.n_.Ld1
	.balign 8
.Ld1$strlab:
	.short	0,1
	.long	0
	.quad	-1,3146
.Ld1:
	.ascii	"zvpjzcpsrwrtlplhjvrkzcjrlvkxalrzaksrhjjmdtcbmrlazht"
	.ascii	"urpvurwchbvrahpwlgpbodpcjdrpywldzqowdrlhmsuhrbrbkdk"
	.ascii	"jzuxvoxclbymjsrdpjxyczmsrzlkqyxaraumhkzyrsmavzjrqrs"
	.ascii	"xwqwvxptqrczkzkodjjaarhpqrxawwqtajjrubsyzwrqzpubqqs"
	.ascii	"brprwxxrschxbbpmuzrskqkrzyklyyvkwyrtlfzjsvpftttwbfz"
	.ascii	"dqfkbypezpjjuxnyopzjmomxwbsdcocxvlykjwekezwvvpyyesp"
	.ascii	"zmdsiajlramrhzkvlrcwydrsmkvpamsrpzvyrqvmysbmmlkrqjc"
	.ascii	"mhmpuzilyppcmssqfccyrjjyuaytrdyuqltlqtdrqcmlmybzwrv"
	.ascii	"ydsttrhhlahqxudrzwthtwjwsrqhtudrzvaqqumyjrmpkptcvpq"
	.ascii	"rjktrzqcsbcrxpycrbajrjkqkzmcyyaryujtjhzrdutjapjtcrp"
	.ascii	"havjrptwkrlrlxidqssajdeddtscvluvewksmljkazivaprtzxr"
	.ascii	"mptqvbxqpyimvzurpaptqxyiqsuoyotrwyajtamzarbraqrldxt"
	.ascii	"wmrmysryjhcwtxtdrdmsxddtaswrmvhjqarukrxdruxrkuykrcj"
	.ascii	"clydrmrhqsjrdlxjrkuxvwxvxmrhprlqwpbldyruudsjrxrlmqk"
	.ascii	"ycrxlsdcsyibmewuvlcwzvezzqteteqsmpybhdseztdytsblkwe"
	.ascii	"mkbzyljdttezumxaezbelhzblmzqwekbatzeyexmdvesueqwjkb"
	.ascii	"jvaqexiwmmxypevuvlckeuwdaqeclskpemuwzhkqeuespxkzjvx"
	.ascii	"ebyhvycwixhcwhcysyitrapmruckppbrvublqhuzujrmpuhsdqr"
	.ascii	"srvzhrbudlprzbaylvrdrtdkdlyzswrmzsjpkkqapratmmudrlm"
	.ascii	"chsmdrsjmxlxxajrzbujjiszsycfxlpbrjrhmrqtsvaksyujrmu"
	.ascii	"ypmmdxvrvqzdqllhrlrstralyzukmmcbrjbmbutapjrvpjmbcrp"
	.ascii	"suypxsrlcbzbspyazrsbzpjbrshjxkyrcxjdhurjmyryjssdtrb"
	.ascii	"ckrvcypsqqaptrprqxvibyolkxwemtutaxlemuscehelybwmeye"
	.ascii	"dbklzcpdwbekqjqzwekyiwurmaxrhvcbdurqvyvbsjivuyzpury"
	.ascii	"jvzjxrubrmbrxclltvsruzvrpphmmjrptvvrdzjqyvximcvatcp"
	.ascii	"apxfuycqikomvdvxubzeqzbyyzwcextxyexxcxcxujejhptupjd"
	.ascii	"ehvhmzkwejealmxxykwxqealxxwzmeykacpazyjeulmpmzcevap"
	.ascii	"abaxijvfpclrartwzuuumdytrwylumhdddkrmvktddbvbbrtjyr"
	.ascii	"jssdxsmziqhcjssosabbqrpjpzjcruxjzrvbcwjxpbmrpluwurv"
	.ascii	"jjwrmtzhasvuumrwvrcmuwarsjsmqwrxjbjvzciykmskfjihmzd"
	.ascii	"crmvbrjcrmthysjsrjhrplbtumramrwhtdiwqbehsbmavwxeusb"
	.ascii	"peyzxxvehecsedmyeuezetypllzjdbqemdscucsdqlewaxmewsw"
	.ascii	"sdetupuhsjiqqquwkhuovhtvyezeulxvyletspqhqesklmyksex"
	.ascii	"vuzhhvkauejjkwqxxuuqecyejtweudeahibzfljrmxlkrpvsrhd"
	.ascii	"vxtzmaryrxuxxrpybibzeseyppeccxthpxvezlcbhiyovrjzltv"
	.ascii	"tdrtvldbhbtcrjzxtsdyqkrtyvpbmwxdcrmturhydxhzmpxqisp"
	.ascii	"ycaxtueuewckwqeajbkjwetsqzsvmviutxsjxblqmfqlyhhddzp"
	.ascii	"urymazzhtxrcxqwcdxwwlrmddxbtdxybrwtxaiwjovwxtzjckkr"
	.ascii	"vxrqysrjlswddwwljrhucvqvilpflqzzbleblbwykcqkjeyazwq"
	.ascii	"wejkhsbdxcexlppwehwykxceqpcmvmbasiktcstlkuccrxpsruy"
	.ascii	"cydjadihlyvovuqrpxqtlpthxrxbujvxphrvzxsyyraxbltlxwd"
	.ascii	"ipbhedzdwtzlklkepqwzdhwwwejjxsmsetwuledevluuwudlses"
	.ascii	"tvzuchqimqqexydzylepejbejbuahqhmsetbuhkejtwwihjqtpu"
	.ascii	"vfvjtcjrmksljpvvrzjluwluzrjuzbiyvbmlzpwuebcyuqbmued"
	.ascii	"hvekztdytquuaeqetvbyicbobhcsqbruwrvhtxhrkipmbtldhby"
	.ascii	"aflwddhrpdykxwswrpisskhocsrwrultujwlsklrxkwwxwdwxwr"
	.ascii	"bwhzcrtrylkqtbdiyvfqzbkhrsrdbmzvwrldssaruxumrarzhbx"
	.ascii	"psdxdiapapwdclqebjcyeplassismeddwamadepeycdwyhlwtwe"
	.ascii	"jbcytxyexktejsvauaqvimzvjkojekemqzvkehxyutqexqqzuet"
	.ascii	"hzlwhjjqpextmyzisjblvfdkkhukcrtwjxvlzmrwjhzjvqipbsx"
	.ascii	"amvcodwjtsmzxrvurwssxtjqxciwttsdkxfbcrtyjbarhpxrkzt"
	.ascii	"ujkjwzwrlkdxyhhprtxrjvmdvpdqaiyosdvrvzlttrzpldcvaqh"
	.ascii	"brqsjksyjhbvraywzrtywrvazxsxpdarjkilakzctdfmuvmwapk"
	.ascii	"bqettdjyvkzxemtpcbcsbevmehajluqcehdvuvmmbdjetmmbihx"
	.ascii	"acwrkyqsjayyurtrchrxhzwujpwsrakmkuctuljrdstitcmeduw"
	.ascii	"axpekzbhhdihbzkpdebassulmuqdetjxzewzvwwaqypqeyexsle"
	.ascii	"xtkxdishvyvoxmeklesbxlpavzekeqdmxexcbvelqehptvmmhhd"
	.ascii	"euyizduppraaazsbrassiqvuabkfvyzahrzkrsqmzmtmwlrajyx"
	.ascii	"jshxkrdprcuiqrvimyyzlomxubjuezzsjkadmebmwbajqhsebuc"
	.ascii	"miacpkdarptakkjkrvzycalvtktrxxzqztsputrzkxzvraspxxk"
	.ascii	"raqmhqsryrvjxkkqvrvcyujkmrkrpxvuvurdzcqartvwyzqdkas"
	.ascii	"rxcvrmvzhblrxvyczrtktsdptvwiutbmdfq\000"
.Le14:
	.size	.Ld1$strlab, .Le14 - .Ld1$strlab
// End asmlist al_const
// Begin asmlist al_typedconsts

.section .data.n_TC_$P$FOREIGN_$$_CODE
	.balign 8
	.type	TC_$P$FOREIGN_$$_CODE,@object
TC_$P$FOREIGN_$$_CODE:
	.quad	.Ld1
.Le15:
	.size	TC_$P$FOREIGN_$$_CODE, .Le15 - TC_$P$FOREIGN_$$_CODE
// End asmlist al_typedconsts
.section .note.GNU-stack,"",%progbits

