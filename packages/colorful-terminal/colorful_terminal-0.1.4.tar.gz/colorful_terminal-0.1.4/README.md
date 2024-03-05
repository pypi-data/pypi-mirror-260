# Colorful Terminal
With the help of ANSI Escape Sequences, this package allows the coloring of the output as well as further sending of commands to the terminal. Highlighting text is thus very simple. It is also possible to update previous lines. This package is an altenative to colorama but provides more options.
This has only been tested on Windows.

## Content
- Installation
- Description
- Usage
- Demonstrations
- Limitations

## Installation
Comming soon

## Description
The model for this package is colorama. However, the standard output is not manipulated here, but appropriate escape characters are inserted into the string. Since the color change is permanent, the colored_print function should be used so that the color settings are reset after each use. Colorama is better developed and tested, but does not offer the color selection that ANSI Escape Sequences allow. 
In addition, this package allows the cursor to be controlled by ANSI escape sequences. So you can also overwrite previous lines or hide the cursor. 

You should just try the demo. There you can see which style adjustments have an effect and which don't work. This also depends on the used terminal.

## Usage
In common usage, the corresponding string of the ANSI escape sequences is prepended to the string. Using the colored_print function will automatically reset all style adjustments. Alternatively Style.RESET_ALL can be used.
```python
colored_print(Fore.RED + "This will be printet in red characters.")
```
```python
colored_print(Back.RED + "This will be printet on a red background.")
```
```python
print(Fore.CYAN + Style.DOUBLY_UNDERLINED + "This text is colored cyan and doubly underlined." + Style.RESET_ALL + " Dieser Text ist völlig normal.")
```
*Most of the available parameters are self-explanatory, so I'll just briefly introduce most of it.*  
**See https://en.wikipedia.org/wiki/ANSI_escape_code for more information.**

## Overview of all the possible color manipulations using **Fore** or **Back**:
- Use **Fore** to manipulate **Foreground Colors**
- Use **Back** to manipulate **Background Colors**
- Normal Colors -> *Parameters* of Fore / Back:
    - `Fore.BLACK`
    - `Fore.RED`
    - `Fore.GREEN`
    - `Fore.YELLOW`
    - `Fore.BLUE`
    - `Fore.MAGENTA`
    - `Fore.CYAN`
    - `Fore.WHITE`
    - `Fore.RESET` -> resets only the foreground / background color

- More intense Colors -> *Parameters* of Fore / Back:
    - `Fore.BRIGHT_BLACK`
    - `Fore.BRIGHT_RED`
    - `Fore.BRIGHT_GREEN`
    - `Fore.BRIGHT_YELLOW`
    - `Fore.BRIGHT_BLUE`
    - `Fore.BRIGHT_MAGENTA`
    - `Fore.BRIGHT_CYAN`
    - `Fore.BRIGHT_WHITE`

- Most intense Colors -> *Parameters* of Fore / Back:
    - `Fore.NEON_RED`
    - `Fore.NEON_GREEN`
    - `Fore.NEON_BLUE`
    - `Fore.NEON_YELLOW`
    - `Fore.NEON_MAGENTA`
    - `Fore.NEON_CYAN`

- *Methods* of Fore / Back:
    - `Fore.rgb(red:int=0, green:int=0, blue:int=0) -> str`  
      Allows you to use any color you can create with the standard 0 to 255 color channels.
    
    - `Fore.color_mode_256(number) -> str`  
      Choose from the 256-color lookup table  
      See https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit for more information.
    
    - `Fore.color_mode_256_demo(colors_per_line:int=32, spacing:int=2) -> None`  
      Prints every of the possible colors in the 256-color lookup table. So you don't have to open your browser to know which number you need for which color.
    
    - `Fore.get_rainbow_string(string:str) -> str`  
      Yes, you can use it to get a string with a rainbow-like gradient. This doesn't print the string.
    
## Overview of all the possible style manipulations using **Style**:
- *Parameters* - probably not all of them will work
    - `Style.RESET_ALL`
    - `Style.BOLD`
    - `Style.DIM`
    - `Style.ITALIC`
    - `Style.UNDERLINED`
    - `Style.CORSSED_OUT`
    - `Style.NORMAL`
    - `Style.DOUBLY_UNDERLINED`
    - `Style.NOT_UNDERLINED`
    - `Style.NOT_CORSSED_OUT`
    - `Style.OVERLINED`
    - `Style.NOT_OVERLINED`
    - `Style.SUPERSCRIPT`
    - `Style.SUBSCRIPT`
    - `Style.NEITHER_SUPERSCRIPT_NOR_SUBSCRIPT`
- *Method*
    - `Style.underline_rgb(red:int=0, green:int=0, blue:int=0) -> str`  
      Will underline with the specified color.

## Overview of all the possible terminal actions using **TermAct**:
- *Parameters*
    - `TermAct.cursor_up`  
      Moves the cursor 1 cell in the given direction. If the cursor is already at the edge of the screen, this has no effect.
    - `TermAct.cursor_down`  
      Moves the cursor 1 cell in the given direction. If the cursor is already at the edge of the screen, this has no effect.
    - `TermAct.cursor_forward`  
      Moves the cursor 1 cell in the given direction. If the cursor is already at the edge of the screen, this has no effect.
    - `TermAct.cursor_back`  
      Moves the cursor 1 cell in the given direction. If the cursor is already at the edge of the screen, this has no effect.
    - `TermAct.cursor_next_line`  
      Moves cursor to beginning of the line 1 line down. (not ANSI.SYS)
    - `TermAct.cursor_previous_line`  
      Moves cursor to beginning of the line 1 line up. (not ANSI.SYS)
    - `TermAct.scroll_up`  
      Scroll whole page up by 1 line. New lines are added at the bottom. (not ANSI.SYS)
    - `TermAct.scroll_down`  
      Scroll whole page down by 1 line. New lines are added at the top. (not ANSI.SYS)
- *Methods*
    - `TermAct.cursor_horizontal_absolute(n=1) -> str`  
      Moves the cursor to column n (default 1). (not ANSI.SYS)
    - `TermAct.cursor_position(n=1, m=1) -> str`  
      Moves the cursor to row n, column m. The values are 1-based, and default to 1 (top left corner) if omitted. A sequence such as CSI ;5H is a synonym for CSI 1;5H as well as CSI 17;H is the same as CSI 17H and CSI 17;1H
    - `TermAct.erase_in_display(n=0) -> str`  
      Clears part of the screen. If n is 0 (or missing), clear from cursor to end of screen. If n is 1, clear from cursor to beginning of the screen. If n is 2, clear entire screen (and moves cursor to upper left on DOS ANSI.SYS). If n is 3, clear entire screen and delete all lines saved in the scrollback buffer (this feature was added for xterm and is supported by other terminal applications).
    - `TermAct.erase_in_line(n=0) -> str`  
      Erases part of the line. If n is 0 (or missing), clear from cursor to the end of the line. If n is 1, clear from cursor to beginning of the line. If n is 2, clear entire line. Cursor position does not change.
    - `TermAct.horizontal_vertical_position(n, m) -> str`  
      Same as CUP, but counts as a format effector function (like CR or LF) rather than an editor function (like CUD or CNL). This can lead to different handling in certain terminal modes.
    - `TermAct.sgr_reset() -> str`  
      Resets colors and style of the characters following this code.
    - `TermAct.save_current_cursor_position() -> str`  
      Saves the cursor position/state in SCO console mode. In vertical split screen mode, instead used to set (as CSI n ; n s) or reset left and right margins.
    - `TermAct.restore_saved_cursor_position() -> str`  
      Restores the cursor position/state in SCO console mode.
    - `TermAct.show_cursor() -> str`  
      Shows the cursor, from the VT220.
    - `TermAct.hide_cursor() -> str`  
      Hides the cursor.
    - `TermAct.undo_line()`  
      Goes one line up and clears the line.
    - `TermAct.clear_current_line()`  
      Clears everything in current line.
    - `clear_terminal()`  
      Clears your terminal with either cls or clear
    - `TermAct.clear_console()`  
      Alias for clear_terminal

## The resetting output function **colored_print**
- colored_print(*args, end="  n", sep=" ")
  Use just like print. Pay attention: Writing `colored_print(Fore.RED, "This is red.")` will print `" This is red."` since the seperator is `" "`. Choose a `+` instaed of the comma to avoid this  
  -> `colored_print(Fore.RED + "This is red.")`  
### If you want to use **print** instead.
Using the print function will not reset your manipulations automatically. You will need to add `Style.RESET_ALL` to reset all changes.

## Demonstrations
There are 6 demo prints (`foreground_demo`, `background_demo`, `style_demo`, `rgb_demo`, `rainbow_demo`, `termact_demo`), the function `demo_print` will call all of them. 
Each demo will show the special effects you can create with this package.  
Here is an image that shows what to expect.
![Demo-Screenshot](images/demo_screenshot.png "Demo-Screenshot")

## Limitations
Some packages like *colorama* and *moviepy* break this package because they manipulate the terminal output, while colorful_terminal does not interfere with other terminal output because the colored_print function always resets the terminal output settings.