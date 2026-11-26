# Të dhënat e programeve KONTURA

Këto skedarë i nxori motori i vërtetë i programeve (15–16.11.2026). Përdori për pamje dhe animacione; mos i vizato shiritat ose kompozimet me dorë.

Njësitë: mm. Koordinatat: X djathtas, Y poshtë (si në SVG).

## LED (Llogaritës LED për Shkronja)
Fushat kryesore: `totalet.m` (metra LED), `totalet.withRes` (me rezervë), `totalet.rolls` (rrotulla), `totalet.strips` (shirita), `cfg` (rregulli, rezerva %, rrotulla m), `kufijte` (gjerësia dhe lartësia e gjithë fjalës), `pjeset[]`: `d` (konturi i shkronjës si SVG path, fill-rule evenodd), `strips` (shiritat si poliline [[x, y], ...]), `led_mm` (LED i shkronjës).

- `led_demo_DRITE.json`: shembulli DRITË, shkronja 40 cm: 12,09 m LED, 12,69 m me 5 % rezervë, 3 rrotulla prej 5 m, 40 shirita.
- `led_KONTURA_inter_30cm.json`: fjala KONTURA me Inter Display Black, 30 cm.
- `led_rregulli.json`: katër vija 60 cm me trashësi 4, 8, 13 dhe 18 cm, të llogaritura veç e veç: 1, 2, 3 dhe 4 shirita (0,56 / 1,12 / 1,67 / 2,22 m).
- `seria2.json` → `format`: zemër 45 × 41 cm 2,61 m, pikë uji 36 × 52 cm 2,75 m, flluskë 43 × 42 cm 3,03 m (mënyra «kontur» u zgjodh vetë nga «auto»).
- `seria2.json` → `alfabeti`: A–Z + Ç Ë me shkronja 20 cm: 13,00 m LED, 74 shirita.

## Kompozimi (Optimizim Kompozimesh)
- `seria2.json` → `reklama_reale`: TIRANA × 3, shkronja 30 cm, fletë 244 × 122 cm, distanca 1 cm, me formën reale: 1,155 m² e zënë, distanca reale min. 10,34 mm, 18 copë.
- `seria2.json` → `reklama_kutite`: e njëjta punë kur çdo shkronjë merret si drejtkëndëshi i saj: 1,438 m². Diferenca: 0,283 m² (19,7 %).
- `nest_KONTURA_mix_2440.json`: 1 × KONTURA 45 cm + 2 × KONTURA 15 cm në fletë 244 × 122 cm, distanca 1 cm.
- `distanca_info.json`: matja e distancës reale më të vogël mes dy pjesëve (për pamjen e zmadhuar).

Kursimi varet nga pjesët (te KONTURA 23,2 %, te REKLAMA × 3 vetëm 11,2 %): mos e jep kurrë si numër të përgjithshëm.

## Shembull
`shembuj/reel_drite.py`: skripti që bëri Reel-in DRITË (1080 × 1920, 11 s, 30 fps): shiritat vizatohen shkronjë pas shkronje dhe numëruesi ngjitet deri te totali i programit. Rrugët e skedarëve duhen përshtatur.
