import glob

"""
byte mazes[64][ROW][COLUMN] = {
    // maze 0
    {
        {...},
    },
    ...
}
"""

ROW = 8
COLUMN = 16

C_MAZE_ARRAY_TEMPLATE = """// This code is auto-make by `maze_c_array_gen.py`.

#define ROW 8
#define COLUMN 16


typedef unsigned char byte;

byte mazes[64][ROW][COLUMN] = {
%s
};

"""

C_BRACES_TEMPLATE = "{%s}"


if __name__ == '__main__':
    
    txt_files = glob.glob('output/data/*.txt')
    txt_files.sort(key=lambda x:len(x))
    
    maze_3d_array = ""
    for i in range(len(txt_files)):
        maze_array_text = ""
        
        with open(txt_files[i], 'r') as f:
            lines = f.readlines()
            
        for x in range(ROW):
            row_text = ""
            n = None
            for y in range(COLUMN):
                # turn to int
                row_text += ("0x0" + lines[x][y])
                if y < COLUMN - 1:
                    row_text += ", "
            row_text = " " * 8 + C_BRACES_TEMPLATE % row_text
            maze_array_text += row_text
            if x < ROW - 1:
                maze_array_text += ',\n'
            else:
                maze_array_text += '\n'
        
        command = ' '*4 + '// maze %d\n'%(i)
        
        maze_array_text = " "*4 + "{\n" + maze_array_text + " "*4 + "}"
        maze_array_text = command + maze_array_text
        
        maze_array_text += ',\n'
        maze_array_text += "    \n"
        
        maze_3d_array += maze_array_text
        
    maze_3d_array += ' '*4 + "// maze 63, design it by yourself!!\n"
    maze_3d_array += ' '*4 + "{{}}"
        
    print(C_MAZE_ARRAY_TEMPLATE % maze_3d_array)
    
    with open('output/maze_array.h', 'w') as f:
        f.write(C_MAZE_ARRAY_TEMPLATE % maze_3d_array)
            
            