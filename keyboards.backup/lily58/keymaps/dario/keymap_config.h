#pragma once

#include "dario.h"
#include "layers.h"

// Lily58 is 58-key (6x4 + 4 thumb keys per side)
// Map 36-key layout to Lily58's full matrix
#define XXX KC_NO

// Wrapper macro to force expansion of LAYER_* macros
#define LAYOUT_wrapper(...) LAYOUT_split_3x5_3(__VA_ARGS__)

// 36-key to 58-key mapping
#define LAYOUT_split_3x5_3(\
     K00, K01, K02, K03, K04,                K05, K06, K07, K08, K09,\
     K10, K11, K12, K13, K14,                K15, K16, K17, K18, K19,\
     K20, K21, K22, K23, K24,                K25, K26, K27, K28, K29,\
                  K32, K33, K34,                K35, K36, K37           \
)\
LAYOUT(\
XXX, XXX, XXX, XXX, XXX, XXX,                XXX, XXX, XXX, XXX, XXX, XXX,\
XXX, K00, K01, K02, K03, K04,                K05, K06, K07, K08, K09, XXX,\
K00, K10, K11, K12, K13, K14,                K15, K16, K17, K18, K19, K09,\
XXX, K20, K21, K22, K23, K24, XXX,      XXX, K25, K26, K27, K28, K29, XXX,\
               XXX, K32, K33, K34,      K35, K36, K37, XXX\
)
