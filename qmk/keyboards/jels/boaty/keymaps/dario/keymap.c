// AUTO-GENERATED - DO NOT EDIT
// Generated from config/keymap.yaml by scripts/generate.py
// Board: Jels Boaty
// Firmware: QMK

#include "dario.h"

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [BASE_NIGHT] = LAYOUT(
        KC_PMNS             , KC_PSLS             , KC_PAST             , KC_P7               , KC_P8               , KC_P9               , KC_P4               , KC_P5               , KC_P6               , KC_PPLS             , KC_P1               , KC_P2               ,
        KC_P3               , KC_PENT             , KC_NUM_LOCK         , KC_P0               , KC_P0               , KC_PDOT             , KC_PENT             , KC_PEQL             , KC_BSPC             , KC_ESC              , KC_TAB              , KC_B                ,
        KC_F                , KC_L                , KC_K                , KC_Q                , KC_P                , KC_G                , KC_O                , KC_U                , KC_DOT              , KC_BSPC             , KC_DEL              , KC_CAPS             ,
        LGUI_T(KC_N)        , LALT_T(KC_S)        , LCTL_T(KC_H)        , LSFT_T(KC_T)        , KC_M                , KC_Y                , RSFT_T(KC_C)        , RCTL_T(KC_A)        , RALT_T(KC_E)        , RGUI_T(KC_I)        , KC_ENT              , KC_X                , KC_V                , KC_J                ,
        KC_D                , KC_Z                , KC_QUOT             , KC_W                , KC_MINS             , KC_SCLN             , KC_COMM             , LT(NUM_NIGHT, KC_BSPC), LT(SYM_NIGHT, KC_R) , LSFT_T(KC_DEL)      , LSFT_T(KC_TAB)      , LT(NAV_NIGHT, KC_SPC), LT(MEDIA_NIGHT, KC_ENT)
    ),
    [BASE_COLEMAK] = LAYOUT(
        KC_PMNS             , KC_PSLS             , KC_PAST             , KC_P7               , KC_P8               , KC_P9               , KC_P4               , KC_P5               , KC_P6               , KC_PPLS             , KC_P1               , KC_P2               ,
        KC_P3               , KC_PENT             , KC_NUM_LOCK         , KC_P0               , KC_PDOT             , KC_PENT             , KC_PEQL             , KC_BSPC             , KC_ESC              , KC_TAB              , KC_Q                , KC_W                ,
        KC_F                , KC_P                , KC_G                , KC_J                , KC_L                , KC_U                , KC_Y                , KC_QUOT             , KC_BSPC             , KC_DEL              , KC_CAPS             , LGUI_T(KC_A)        ,
        LALT_T(KC_R)        , LCTL_T(KC_S)        , LSFT_T(KC_T)        , KC_D                , KC_H                , RSFT_T(KC_N)        , RCTL_T(KC_E)        , RALT_T(KC_I)        , RGUI_T(KC_O)        , KC_ENT              , KC_LSFT             , KC_Z                , KC_X                , KC_C                ,
        KC_V                , KC_B                , KC_K                , KC_M                , KC_COMM             , KC_DOT              , KC_SLSH             , KC_ENT              , LT(NAV, KC_SPC)     , LT(MEDIA, KC_TAB)   , LT(SYM, KC_DEL)     , KC_LSFT             , LT(NUM, KC_BSPC)    
    ),
    [NUM] = LAYOUT(
        KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             ,
        KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_LBRC             ,
        KC_4                , KC_5                , KC_6                , KC_RBRC             , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_TRNS             , KC_TRNS             , KC_TRNS             ,
        KC_SLSH             , KC_1                , KC_2                , KC_3                , KC_EQL              , KC_NO               , KC_LSFT             , KC_LCTL             , KC_LALT             , KC_LGUI             , KC_TRNS             , KC_GRV              , KC_7                , KC_8                ,
        KC_9                , KC_BSLS             , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_COLN             , KC_0                , KC_MINS             , KC_NO               , KC_NO               , KC_NO               
    ),
    [SYM] = LAYOUT(
        KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             ,
        KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_LCBR             ,
        KC_DLR              , KC_PERC             , KC_CIRC             , KC_RCBR             , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_TRNS             , KC_TRNS             , KC_TRNS             ,
        KC_QUES             , KC_EXLM             , KC_AT               , KC_HASH             , KC_PLUS             , KC_NO               , KC_LSFT             , KC_LCTL             , KC_LALT             , KC_LGUI             , KC_TRNS             , KC_TILD             , KC_AMPR             , KC_ASTR             ,
        KC_COLN             , KC_PIPE             , QK_BOOT             , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_LPRN             , KC_RPRN             , KC_UNDS             , KC_NO               , KC_NO               , KC_NO               
    ),
    [NAV] = LAYOUT(
        KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             ,
        KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_NO               ,
        KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_ESC              , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_TRNS             , KC_TRNS             , KC_TRNS             ,
        KC_LGUI             , KC_LALT             , KC_LCTL             , KC_LSFT             , KC_NO               , KC_CAPS             , KC_LEFT             , KC_DOWN             , KC_UP               , KC_RGHT             , KC_TRNS             , LGUI(KC_Z)          , LGUI(KC_X)          , LGUI(KC_C)          ,
        LGUI(KC_V)          , SGUI(KC_Z)          , KC_INS              , KC_HOME             , KC_PGDN             , KC_PGUP             , KC_END              , KC_NO               , KC_NO               , KC_NO               , KC_DEL              , KC_ENT              , KC_BSPC             
    ),
    [MEDIA] = LAYOUT(
        KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             ,
        KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , DF(BASE_NIGHT)      ,
        DF(BASE_COLEMAK)    , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_TRNS             , KC_TRNS             , KC_TRNS             ,
        KC_LGUI             , KC_LALT             , KC_LCTL             , KC_LSFT             , KC_NO               , KC_NO               , KC_MPRV             , KC_VOLD             , KC_VOLU             , KC_MNXT             , KC_TRNS             , KC_NO               , KC_NO               , KC_NO               ,
        KC_NO               , QK_BOOT             , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_MSTP             , KC_MPLY             , KC_MUTE             
    ),
    [FUN] = LAYOUT(
        KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             ,
        KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_F12              ,
        KC_F7               , KC_F8               , KC_F9               , KC_PSCR             , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_TRNS             , KC_TRNS             , KC_TRNS             ,
        KC_F11              , KC_F4               , KC_F5               , KC_F6               , KC_SCRL             , KC_NO               , KC_LSFT             , KC_LCTL             , KC_LALT             , KC_LGUI             , KC_TRNS             , KC_F10              , KC_F1               , KC_F2               ,
        KC_F3               , KC_PAUS             , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_APP              , KC_SPC              , KC_TAB              , KC_NO               , KC_NO               , KC_NO               
    ),
    [NUM_NIGHT] = LAYOUT(
        KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             ,
        KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TILD             ,
        KC_LBRC             , KC_RBRC             , KC_PERC             , KC_NO               , KC_CIRC             , KC_7                , KC_8                , KC_9                , KC_DOT              , KC_TRNS             , KC_TRNS             , KC_TRNS             ,
        KC_LGUI             , KC_LALT             , KC_LCTL             , KC_LSFT             , KC_PIPE             , KC_HASH             , KC_4                , KC_5                , KC_6                , KC_GRV              , KC_TRNS             , LGUI(KC_Z)          , LGUI(KC_X)          , LGUI(KC_C)          ,
        LGUI(KC_V)          , SGUI(KC_Z)          , KC_DLR              , KC_1                , KC_2                , KC_3                , KC_COMM             , KC_NO               , KC_NO               , KC_NO               , KC_COLN             , KC_0                , KC_AT               
    ),
    [SYM_NIGHT] = LAYOUT(
        KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             ,
        KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_PERC             ,
        KC_ASTR             , KC_DLR              , KC_DQUO             , KC_NO               , KC_PLUS             , KC_LT               , KC_LCBR             , KC_RCBR             , KC_GT               , KC_TRNS             , KC_TRNS             , KC_TRNS             ,
        KC_LGUI             , KC_LALT             , KC_LCTL             , KC_LSFT             , KC_BSLS             , KC_EXLM             , KC_EQL              , KC_LPRN             , KC_RPRN             , KC_SCLN             , KC_TRNS             , KC_NO               , KC_NO               , KC_NO               ,
        KC_AMPR             , KC_NO               , KC_UNDS             , KC_MINS             , KC_LBRC             , KC_RBRC             , KC_COLN             , KC_NO               , KC_NO               , KC_NO               , KC_QUES             , KC_SPC              , KC_SLSH             
    ),
    [NAV_NIGHT] = LAYOUT(
        KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             ,
        KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_NO               ,
        KC_PGUP             , KC_NO               , KC_NO               , KC_ESC              , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_TRNS             , KC_TRNS             , KC_TRNS             ,
        KC_NO               , KC_LEFT             , KC_UP               , KC_RGHT             , KC_CAPS             , KC_NO               , KC_LSFT             , KC_LCTL             , KC_LALT             , KC_LGUI             , KC_TRNS             , KC_END              , KC_PGDN             , KC_DOWN             ,
        KC_HOME             , KC_INS              , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_BSPC             , KC_ENT              , KC_DEL              , KC_NO               , KC_NO               , KC_NO               
    ),
    [MEDIA_NIGHT] = LAYOUT(
        KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             ,
        KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , KC_TRNS             , DF(BASE_NIGHT)      ,
        DF(BASE_COLEMAK)    , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_NO               , KC_TRNS             , KC_TRNS             , KC_TRNS             ,
        KC_MNXT             , KC_VOLU             , KC_VOLD             , KC_MPRV             , KC_NO               , KC_NO               , KC_LSFT             , KC_LCTL             , KC_LALT             , KC_LGUI             , KC_TRNS             , LGUI(KC_Z)          , LGUI(KC_X)          , LGUI(KC_C)          ,
        LGUI(KC_V)          , SGUI(KC_Z)          , KC_NO               , KC_NO               , KC_NO               , KC_NO               , QK_BOOT             , KC_MUTE             , KC_MPLY             , KC_MSTP             , KC_NO               , KC_NO               , KC_NO               
    ),
};
