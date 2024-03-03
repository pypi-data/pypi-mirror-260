from textwrap import dedent

from kalamine import KeyboardLayout
from kalamine.template import klc_deadkeys, klc_dk_index, klc_keymap

from .util import get_layout_dict


def split(multiline_str: str):
    return dedent(multiline_str).lstrip().rstrip().splitlines()


LAYOUTS = {}
for filename in ["ansi", "intl", "prog"]:
    LAYOUTS[filename] = KeyboardLayout(get_layout_dict(filename))


def test_ansi_keymap():
    keymap = klc_keymap(LAYOUTS["ansi"])
    assert len(keymap) == 49
    assert keymap == split(
        """
        02	1	0	1	0021	-1	-1	// 1 !
        03	2	0	2	0040	-1	-1	// 2 @
        04	3	0	3	0023	-1	-1	// 3 #
        05	4	0	4	0024	-1	-1	// 4 $
        06	5	0	5	0025	-1	-1	// 5 %
        07	6	0	6	005e	-1	-1	// 6 ^
        08	7	0	7	0026	-1	-1	// 7 &
        09	8	0	8	002a	-1	-1	// 8 *
        0a	9	0	9	0028	-1	-1	// 9 (
        0b	0	0	0	0029	-1	-1	// 0 )
        10	Q	1	q	Q	-1	-1	// q Q
        11	W	1	w	W	-1	-1	// w W
        12	E	1	e	E	-1	-1	// e E
        13	R	1	r	R	-1	-1	// r R
        14	T	1	t	T	-1	-1	// t T
        15	Y	1	y	Y	-1	-1	// y Y
        16	U	1	u	U	-1	-1	// u U
        17	I	1	i	I	-1	-1	// i I
        18	O	1	o	O	-1	-1	// o O
        19	P	1	p	P	-1	-1	// p P
        1e	A	1	a	A	-1	-1	// a A
        1f	S	1	s	S	-1	-1	// s S
        20	D	1	d	D	-1	-1	// d D
        21	F	1	f	F	-1	-1	// f F
        22	G	1	g	G	-1	-1	// g G
        23	H	1	h	H	-1	-1	// h H
        24	J	1	j	J	-1	-1	// j J
        25	K	1	k	K	-1	-1	// k K
        26	L	1	l	L	-1	-1	// l L
        27	OEM_1	0	003b	003a	-1	-1	// ; :
        2c	Z	1	z	Z	-1	-1	// z Z
        2d	X	1	x	X	-1	-1	// x X
        2e	C	1	c	C	-1	-1	// c C
        2f	V	1	v	V	-1	-1	// v V
        30	B	1	b	B	-1	-1	// b B
        31	N	1	n	N	-1	-1	// n N
        32	M	1	m	M	-1	-1	// m M
        33	OEM_COMMA	0	002c	003c	-1	-1	// , <
        34	OEM_PERIOD	0	002e	003e	-1	-1	// . >
        35	OEM_2	0	002f	003f	-1	-1	// / ?
        0c	OEM_MINUS	0	002d	005f	-1	-1	// - _
        0d	OEM_PLUS	0	003d	002b	-1	-1	// = +
        1a	OEM_3	0	005b	007b	-1	-1	// [ {
        1b	OEM_4	0	005d	007d	-1	-1	// ] }
        28	OEM_5	0	0027	0022	-1	-1	// ' "
        29	OEM_6	0	0060	007e	-1	-1	// ` ~
        2b	OEM_7	0	005c	007c	-1	-1	// \\ |
        56	OEM_102	0	-1	-1	-1	-1	//
        39	SPACE	0	0020	0020	-1	-1	//
        """
    )


def test_ansi_deadkeys():
    assert len(klc_dk_index(LAYOUTS["ansi"])) == 0
    assert len(klc_deadkeys(LAYOUTS["ansi"])) == 0


def test_intl_keymap():
    keymap = klc_keymap(LAYOUTS["intl"])
    assert len(keymap) == 49
    assert keymap == split(
        """
        02	1	0	1	0021	-1	-1	// 1 !
        03	2	0	2	0040	-1	-1	// 2 @
        04	3	0	3	0023	-1	-1	// 3 #
        05	4	0	4	0024	-1	-1	// 4 $
        06	5	0	5	0025	-1	-1	// 5 %
        07	6	0	6	005e@	-1	-1	// 6 ^
        08	7	0	7	0026	-1	-1	// 7 &
        09	8	0	8	002a	-1	-1	// 8 *
        0a	9	0	9	0028	-1	-1	// 9 (
        0b	0	0	0	0029	-1	-1	// 0 )
        10	Q	1	q	Q	-1	-1	// q Q
        11	W	1	w	W	-1	-1	// w W
        12	E	1	e	E	-1	-1	// e E
        13	R	1	r	R	-1	-1	// r R
        14	T	1	t	T	-1	-1	// t T
        15	Y	1	y	Y	-1	-1	// y Y
        16	U	1	u	U	-1	-1	// u U
        17	I	1	i	I	-1	-1	// i I
        18	O	1	o	O	-1	-1	// o O
        19	P	1	p	P	-1	-1	// p P
        1e	A	1	a	A	-1	-1	// a A
        1f	S	1	s	S	-1	-1	// s S
        20	D	1	d	D	-1	-1	// d D
        21	F	1	f	F	-1	-1	// f F
        22	G	1	g	G	-1	-1	// g G
        23	H	1	h	H	-1	-1	// h H
        24	J	1	j	J	-1	-1	// j J
        25	K	1	k	K	-1	-1	// k K
        26	L	1	l	L	-1	-1	// l L
        27	OEM_1	0	003b	003a	-1	-1	// ; :
        2c	Z	1	z	Z	-1	-1	// z Z
        2d	X	1	x	X	-1	-1	// x X
        2e	C	1	c	C	-1	-1	// c C
        2f	V	1	v	V	-1	-1	// v V
        30	B	1	b	B	-1	-1	// b B
        31	N	1	n	N	-1	-1	// n N
        32	M	1	m	M	-1	-1	// m M
        33	OEM_COMMA	0	002c	003c	-1	-1	// , <
        34	OEM_PERIOD	0	002e	003e	-1	-1	// . >
        35	OEM_2	0	002f	003f	-1	-1	// / ?
        0c	OEM_MINUS	0	002d	005f	-1	-1	// - _
        0d	OEM_PLUS	0	003d	002b	-1	-1	// = +
        1a	OEM_3	0	005b	007b	-1	-1	// [ {
        1b	OEM_4	0	005d	007d	-1	-1	// ] }
        28	OEM_5	0	0027@	0022@	-1	-1	// ' "
        29	OEM_6	0	0060@	007e@	-1	-1	// ` ~
        2b	OEM_7	0	005c	007c	-1	-1	// \\ |
        56	OEM_102	0	005c	007c	-1	-1	// \\ |
        39	SPACE	0	0020	0020	-1	-1	//
        """
    )


def test_intl_deadkeys():
    dk_index = klc_dk_index(LAYOUTS["intl"])
    assert len(dk_index) == 5
    assert dk_index == split(
        """
        0027	"1DK"
        0060	"GRAVE"
        005e	"CIRCUMFLEX"
        007e	"TILDE"
        0022	"DIAERESIS"
        """
    )

    deadkeys = klc_deadkeys(LAYOUTS["intl"])
    # assert len(deadkeys) == 138
    assert deadkeys == split(
        """
        // DEADKEY: 1DK //{{{
        DEADKEY	0027
        0027	0027	// ' -> '
        0045	00c9	// E -> É
        0065	00e9	// e -> é
        0055	00da	// U -> Ú
        0075	00fa	// u -> ú
        0049	00cd	// I -> Í
        0069	00ed	// i -> í
        004f	00d3	// O -> Ó
        006f	00f3	// o -> ó
        0041	00c1	// A -> Á
        0061	00e1	// a -> á
        0043	00c7	// C -> Ç
        0063	00e7	// c -> ç
        002e	2026	// . -> …
        0020	0027	//   -> '
        //}}}

        // DEADKEY: GRAVE //{{{
        DEADKEY	0060
        0041	00c0	// A -> À
        0061	00e0	// a -> à
        0045	00c8	// E -> È
        0065	00e8	// e -> è
        0049	00cc	// I -> Ì
        0069	00ec	// i -> ì
        004e	01f8	// N -> Ǹ
        006e	01f9	// n -> ǹ
        004f	00d2	// O -> Ò
        006f	00f2	// o -> ò
        0055	00d9	// U -> Ù
        0075	00f9	// u -> ù
        0057	1e80	// W -> Ẁ
        0077	1e81	// w -> ẁ
        0059	1ef2	// Y -> Ỳ
        0079	1ef3	// y -> ỳ
        0020	0060	//   -> `
        //}}}

        // DEADKEY: CIRCUMFLEX //{{{
        DEADKEY	005e
        0041	00c2	// A -> Â
        0061	00e2	// a -> â
        0043	0108	// C -> Ĉ
        0063	0109	// c -> ĉ
        0045	00ca	// E -> Ê
        0065	00ea	// e -> ê
        0047	011c	// G -> Ĝ
        0067	011d	// g -> ĝ
        0048	0124	// H -> Ĥ
        0068	0125	// h -> ĥ
        0049	00ce	// I -> Î
        0069	00ee	// i -> î
        004a	0134	// J -> Ĵ
        006a	0135	// j -> ĵ
        004f	00d4	// O -> Ô
        006f	00f4	// o -> ô
        0053	015c	// S -> Ŝ
        0073	015d	// s -> ŝ
        0055	00db	// U -> Û
        0075	00fb	// u -> û
        0057	0174	// W -> Ŵ
        0077	0175	// w -> ŵ
        0059	0176	// Y -> Ŷ
        0079	0177	// y -> ŷ
        005a	1e90	// Z -> Ẑ
        007a	1e91	// z -> ẑ
        0030	2070	// 0 -> ⁰
        0031	00b9	// 1 -> ¹
        0032	00b2	// 2 -> ²
        0033	00b3	// 3 -> ³
        0034	2074	// 4 -> ⁴
        0035	2075	// 5 -> ⁵
        0036	2076	// 6 -> ⁶
        0037	2077	// 7 -> ⁷
        0038	2078	// 8 -> ⁸
        0039	2079	// 9 -> ⁹
        0028	207d	// ( -> ⁽
        0029	207e	// ) -> ⁾
        002b	207a	// + -> ⁺
        002d	207b	// - -> ⁻
        003d	207c	// = -> ⁼
        0020	005e	//   -> ^
        //}}}

        // DEADKEY: TILDE //{{{
        DEADKEY	007e
        0041	00c3	// A -> Ã
        0061	00e3	// a -> ã
        0045	1ebc	// E -> Ẽ
        0065	1ebd	// e -> ẽ
        0049	0128	// I -> Ĩ
        0069	0129	// i -> ĩ
        004e	00d1	// N -> Ñ
        006e	00f1	// n -> ñ
        004f	00d5	// O -> Õ
        006f	00f5	// o -> õ
        0055	0168	// U -> Ũ
        0075	0169	// u -> ũ
        0056	1e7c	// V -> Ṽ
        0076	1e7d	// v -> ṽ
        0059	1ef8	// Y -> Ỹ
        0079	1ef9	// y -> ỹ
        003c	2272	// < -> ≲
        003e	2273	// > -> ≳
        003d	2243	// = -> ≃
        0020	007e	//   -> ~
        //}}}

        // DEADKEY: DIAERESIS //{{{
        DEADKEY	0022
        0041	00c4	// A -> Ä
        0061	00e4	// a -> ä
        0045	00cb	// E -> Ë
        0065	00eb	// e -> ë
        0048	1e26	// H -> Ḧ
        0068	1e27	// h -> ḧ
        0049	00cf	// I -> Ï
        0069	00ef	// i -> ï
        004f	00d6	// O -> Ö
        006f	00f6	// o -> ö
        0074	1e97	// t -> ẗ
        0055	00dc	// U -> Ü
        0075	00fc	// u -> ü
        0057	1e84	// W -> Ẅ
        0077	1e85	// w -> ẅ
        0058	1e8c	// X -> Ẍ
        0078	1e8d	// x -> ẍ
        0059	0178	// Y -> Ÿ
        0079	00ff	// y -> ÿ
        0020	0022	//   -> "
        //}}}
        """
    )


def test_prog_keymap():
    keymap = klc_keymap(LAYOUTS["prog"])
    assert len(keymap) == 49
    assert keymap == split(
        """
        02	1	0	1	0021	-1	-1	0021	-1	// 1 ! !
        03	2	0	2	0040	-1	-1	0028	-1	// 2 @ (
        04	3	0	3	0023	-1	-1	0029	-1	// 3 # )
        05	4	0	4	0024	-1	-1	0027	-1	// 4 $ '
        06	5	0	5	0025	-1	-1	0022	-1	// 5 % "
        07	6	0	6	005e	-1	-1	005e@	-1	// 6 ^ ^
        08	7	0	7	0026	-1	-1	7	-1	// 7 & 7
        09	8	0	8	002a	-1	-1	8	-1	// 8 * 8
        0a	9	0	9	0028	-1	-1	9	-1	// 9 ( 9
        0b	0	0	0	0029	-1	-1	002f	-1	// 0 ) /
        10	Q	1	q	Q	-1	-1	003d	-1	// q Q =
        11	W	1	w	W	-1	-1	003c	2264	// w W < ≤
        12	E	1	e	E	-1	-1	003e	2265	// e E > ≥
        13	R	1	r	R	-1	-1	002d	-1	// r R -
        14	T	1	t	T	-1	-1	002b	-1	// t T +
        15	Y	1	y	Y	-1	-1	-1	-1	// y Y
        16	U	1	u	U	-1	-1	4	-1	// u U 4
        17	I	1	i	I	-1	-1	5	-1	// i I 5
        18	O	1	o	O	-1	-1	6	-1	// o O 6
        19	P	1	p	P	-1	-1	002a	-1	// p P *
        1e	A	1	a	A	-1	-1	007b	-1	// a A {
        1f	S	1	s	S	-1	-1	005b	-1	// s S [
        20	D	1	d	D	-1	-1	005d	-1	// d D ]
        21	F	1	f	F	-1	-1	007d	-1	// f F }
        22	G	1	g	G	-1	-1	002f	-1	// g G /
        23	H	1	h	H	-1	-1	-1	-1	// h H
        24	J	1	j	J	-1	-1	1	-1	// j J 1
        25	K	1	k	K	-1	-1	2	-1	// k K 2
        26	L	1	l	L	-1	-1	3	-1	// l L 3
        27	OEM_1	0	003b	003a	-1	-1	002d	-1	// ; : -
        2c	Z	1	z	Z	-1	-1	007e	-1	// z Z ~
        2d	X	1	x	X	-1	-1	0060	-1	// x X `
        2e	C	1	c	C	-1	-1	007c	00a6	// c C | ¦
        2f	V	1	v	V	-1	-1	005f	-1	// v V _
        30	B	1	b	B	-1	-1	005c	-1	// b B \\
        31	N	1	n	N	-1	-1	-1	-1	// n N
        32	M	1	m	M	-1	-1	0	-1	// m M 0
        33	OEM_COMMA	0	002c	003c	-1	-1	002c	-1	// , < ,
        34	OEM_PERIOD	0	002e	003e	-1	-1	002e	-1	// . > .
        35	OEM_2	0	002f	003f	-1	-1	002b	-1	// / ? +
        0c	OEM_MINUS	0	002d	005f	-1	-1	-1	-1	// - _
        0d	OEM_PLUS	0	003d	002b	-1	-1	-1	-1	// = +
        1a	OEM_3	0	005b	007b	-1	-1	-1	-1	// [ {
        1b	OEM_4	0	005d	007d	-1	-1	-1	-1	// ] }
        28	OEM_5	0	0027	0022	-1	-1	0027@	0022@	// ' " ' "
        29	OEM_6	0	0060	007e	-1	-1	0060@	007e@	// ` ~ ` ~
        2b	OEM_7	0	005c	007c	-1	-1	-1	-1	// \\ |
        56	OEM_102	0	-1	-1	-1	-1	-1	-1	//
        39	SPACE	0	0020	0020	-1	-1	0020	0020	//
        """
    )


def test_prog_deadkeys():
    dk_index = klc_dk_index(LAYOUTS["prog"])
    assert len(dk_index) == 5
    assert dk_index == split(
        """
        0060	"GRAVE"
        0027	"ACUTE"
        005e	"CIRCUMFLEX"
        007e	"TILDE"
        0022	"DIAERESIS"
        """
    )

    deadkeys = klc_deadkeys(LAYOUTS["prog"])
    assert len(deadkeys) == 153
    assert deadkeys == split(
        """
        // DEADKEY: GRAVE //{{{
        DEADKEY	0060
        0041	00c0	// A -> À
        0061	00e0	// a -> à
        0045	00c8	// E -> È
        0065	00e8	// e -> è
        0049	00cc	// I -> Ì
        0069	00ec	// i -> ì
        004e	01f8	// N -> Ǹ
        006e	01f9	// n -> ǹ
        004f	00d2	// O -> Ò
        006f	00f2	// o -> ò
        0055	00d9	// U -> Ù
        0075	00f9	// u -> ù
        0057	1e80	// W -> Ẁ
        0077	1e81	// w -> ẁ
        0059	1ef2	// Y -> Ỳ
        0079	1ef3	// y -> ỳ
        0020	0060	//   -> `
        //}}}

        // DEADKEY: ACUTE //{{{
        DEADKEY	0027
        0041	00c1	// A -> Á
        0061	00e1	// a -> á
        0043	0106	// C -> Ć
        0063	0107	// c -> ć
        0045	00c9	// E -> É
        0065	00e9	// e -> é
        0047	01f4	// G -> Ǵ
        0067	01f5	// g -> ǵ
        0049	00cd	// I -> Í
        0069	00ed	// i -> í
        004b	1e30	// K -> Ḱ
        006b	1e31	// k -> ḱ
        004c	0139	// L -> Ĺ
        006c	013a	// l -> ĺ
        004d	1e3e	// M -> Ḿ
        006d	1e3f	// m -> ḿ
        004e	0143	// N -> Ń
        006e	0144	// n -> ń
        004f	00d3	// O -> Ó
        006f	00f3	// o -> ó
        0050	1e54	// P -> Ṕ
        0070	1e55	// p -> ṕ
        0052	0154	// R -> Ŕ
        0072	0155	// r -> ŕ
        0053	015a	// S -> Ś
        0073	015b	// s -> ś
        0055	00da	// U -> Ú
        0075	00fa	// u -> ú
        0057	1e82	// W -> Ẃ
        0077	1e83	// w -> ẃ
        0059	00dd	// Y -> Ý
        0079	00fd	// y -> ý
        005a	0179	// Z -> Ź
        007a	017a	// z -> ź
        0020	0027	//   -> '
        //}}}

        // DEADKEY: CIRCUMFLEX //{{{
        DEADKEY	005e
        0041	00c2	// A -> Â
        0061	00e2	// a -> â
        0043	0108	// C -> Ĉ
        0063	0109	// c -> ĉ
        0045	00ca	// E -> Ê
        0065	00ea	// e -> ê
        0047	011c	// G -> Ĝ
        0067	011d	// g -> ĝ
        0048	0124	// H -> Ĥ
        0068	0125	// h -> ĥ
        0049	00ce	// I -> Î
        0069	00ee	// i -> î
        004a	0134	// J -> Ĵ
        006a	0135	// j -> ĵ
        004f	00d4	// O -> Ô
        006f	00f4	// o -> ô
        0053	015c	// S -> Ŝ
        0073	015d	// s -> ŝ
        0055	00db	// U -> Û
        0075	00fb	// u -> û
        0057	0174	// W -> Ŵ
        0077	0175	// w -> ŵ
        0059	0176	// Y -> Ŷ
        0079	0177	// y -> ŷ
        005a	1e90	// Z -> Ẑ
        007a	1e91	// z -> ẑ
        0030	2070	// 0 -> ⁰
        0031	00b9	// 1 -> ¹
        0032	00b2	// 2 -> ²
        0033	00b3	// 3 -> ³
        0034	2074	// 4 -> ⁴
        0035	2075	// 5 -> ⁵
        0036	2076	// 6 -> ⁶
        0037	2077	// 7 -> ⁷
        0038	2078	// 8 -> ⁸
        0039	2079	// 9 -> ⁹
        0028	207d	// ( -> ⁽
        0029	207e	// ) -> ⁾
        002b	207a	// + -> ⁺
        002d	207b	// - -> ⁻
        003d	207c	// = -> ⁼
        0020	005e	//   -> ^
        //}}}

        // DEADKEY: TILDE //{{{
        DEADKEY	007e
        0041	00c3	// A -> Ã
        0061	00e3	// a -> ã
        0045	1ebc	// E -> Ẽ
        0065	1ebd	// e -> ẽ
        0049	0128	// I -> Ĩ
        0069	0129	// i -> ĩ
        004e	00d1	// N -> Ñ
        006e	00f1	// n -> ñ
        004f	00d5	// O -> Õ
        006f	00f5	// o -> õ
        0055	0168	// U -> Ũ
        0075	0169	// u -> ũ
        0056	1e7c	// V -> Ṽ
        0076	1e7d	// v -> ṽ
        0059	1ef8	// Y -> Ỹ
        0079	1ef9	// y -> ỹ
        003c	2272	// < -> ≲
        003e	2273	// > -> ≳
        003d	2243	// = -> ≃
        0020	007e	//   -> ~
        //}}}

        // DEADKEY: DIAERESIS //{{{
        DEADKEY	0022
        0041	00c4	// A -> Ä
        0061	00e4	// a -> ä
        0045	00cb	// E -> Ë
        0065	00eb	// e -> ë
        0048	1e26	// H -> Ḧ
        0068	1e27	// h -> ḧ
        0049	00cf	// I -> Ï
        0069	00ef	// i -> ï
        004f	00d6	// O -> Ö
        006f	00f6	// o -> ö
        0074	1e97	// t -> ẗ
        0055	00dc	// U -> Ü
        0075	00fc	// u -> ü
        0057	1e84	// W -> Ẅ
        0077	1e85	// w -> ẅ
        0058	1e8c	// X -> Ẍ
        0078	1e8d	// x -> ẍ
        0059	0178	// Y -> Ÿ
        0079	00ff	// y -> ÿ
        0020	0022	//   -> "
        //}}}
        """
    )
