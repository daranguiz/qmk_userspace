## Things to type that bother me 

- `1:1`. Chording with R and L at the same time, with R thumb moving.
- `arr[N]`. Chord -> letter -> chord 

## QMK and ZMK common repo 

I have this repo, QMK userspace, as well as a separate ZMK repo. Right now, I have to maintain these two manually. If I make a change in one, I have to make a change in the other. It's a very manual process, very error prone, and usually just means my keymaps get out of date.

I want to merge these into a single repo (or have a submodule or something, really whatever fits the model best), and I want to have a single common place where I can update my keymap. After I do so, it should auto-codegen for both QMK and ZMK. 

Repo requirements:

 - This should be a new repo, and as a user, it should feel like I'm only using one repo. Under the hood, I'm okay if it's literally one repo (with config + qmk + zmk), or if it's just a config repo with git submodules individually for qmk and zmk. I understand that things like github actions, upstream syncing, etc may be harder if it's all one repo, so I'm okay with the submodule approach if that's the best option.
 - I do not care about preserving git history until this point. If the migration loses history, that is fine.

Functional requirements:

 - We can assume that I have a core 3x5_3 layout. I may deviate from this and add more keys at some point in the future, so we should make it somewhat easy to change that core layout size. 
 - The keymap itself should never deviate between QMK and ZMK. This includes mod keys, layer tap keys, etc. One button should do the same thing across all keyboards, with some exceptions below. (Note that I also want things like bootloader keys to stay consistent).
 - Exceptions to the rule above:
    - ZMK boards may have bluetooth, whereas qmk does not. There may be some extra keys done for the BT keyboards that should not appear on qmk. I still want to use a common layout though, so I will specify the BT actions in the top-level keymap, then I want them stripped when we down-compile for QMK. 
    - Larger boards with more keys may want to add additional buttons to the keymap. That should be done on a per-keyboard basis. (And related: this per-keyboard distinction should happen at the higher config layer, not the qmk or zmk layer. I think it would be useful for the QMK/ZMK layer to be completely codegen'd. I'm not against going into the individual keymap itself and making those kinds of per-board layout changes, but I'm concerned about fighting with the codegen and having my changes get wiped away by codegen). 
 - Things that are not keymap-specific should fall to the purview of the individual repo or keyboard itself. Some examples:
    - I have been playing with homerow mods a lot. QMK and ZMK have different homerow mod functionality. While I'm manually trying to get them to be similar, I want their configurations to be kept separate from one another so I can tweak them. (This may change in the future).
    - Things like OLED screens, encoders, etc are all very keyboard-specific. Those must be managed on a per-board basis. 
    - Things like bootmagic in QMK may deviate. (Bootmagic operates on the matrix row/col, not on the key position, so it may change depending on the size of the board. Moreover, idk if ZMK has bootmagic. For ZMK, I always use the bootloader button itself). 
 - Adding new boards, potentially with different sizes than what I have already, has to be easy.

