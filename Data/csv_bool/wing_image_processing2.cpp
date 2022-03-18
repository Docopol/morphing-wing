#include <iostream>
#include <string>
#include <algorithm>
#include <windows.h>
#include <cmath>
#include <fstream>


//global variables

int w_tot = 0;
int h_tot = 0;

static HWND sHwnd;

struct px_color
{
    int r;
    int g;
    int b;
};

//rbg image storage
px_color rgb_img[4272][2848];
bool bool_img[4272][2848];

//reference color for pixel seeking
px_color ref_rgb = {230, 101, 43};

//default tolerance and multiplier for them
px_color ref_tolerance = {10, 10, 10};

float multiplier = 2;


void load_BMP(char* filename)
{
    int i;
    FILE* f = fopen(filename, "rb");
    unsigned char info[54];

    // read the 54-byte header
    fread(info, sizeof(unsigned char), 54, f);

    typedef unsigned char uc;
    // extract image height and width from header
    int img_width = *(int*)&info[18];
    int img_height = *(int*)&info[22];

    w_tot = img_width;
    h_tot = img_height;

    int bpp = 24; // gonna assume 24 bits per pixel
    int row_size = (((bpp * img_width) + 31) / 32) * 4; // this is the size of each row in 32 bit words
    uc* data = new uc[img_height * row_size]; // all lines and with padded rows

    fread(data, sizeof(uc), img_height * row_size, f);
    fclose(f);

    uc** image = new uc* [img_height]; // allocate number of lines in the file

    std::cout << w_tot << " " << h_tot << std::endl;
    for (int i = 0; i < img_height; ++i)
    {
        int row = img_height - (i + 1); // so we can invert the row, we do the bottom -> top inversion here.
        image[row] = new uc[row_size]; // allocate the rows, will copy the padding but that is fine, we can ignore it later
        memcpy(image[row], &data[i * row_size], row_size); // copy each row
    }

    //loop that loads the image into global array
    for( int y = 0; y < img_height; y++ )
    {
        for( int x = 0; x < img_width; x++ )
        {
            //load the actual px color data
                rgb_img[y][x].r = image[y][(x+1)*3+2];
                rgb_img[y][x].g = image[y][(x+1)*3+1];
                rgb_img[y][x].b = image[y][(x+1)*3+0];
        }
    }
    std::cout << "image loaded successfully." << std::endl;
}


void bool_init_pass()
{
    for( int x_1 = 0; x_1 < w_tot; x_1++)
    {
        for( int y_1 = 0; y_1 < h_tot; y_1++)
        {
            //check r value
                if( rgb_img[x_1][y_1].r <= (ref_rgb.r+ref_tolerance.r) && rgb_img[x_1][y_1].r >= (ref_rgb.r-ref_tolerance.r))
                {
                //if(rgb_img[x_1-1][y_1-1].r <= (ref_rgb.r+ref_tolerance.r*multiplier) && rgb_img[x_1-1][y_1-1].r >= (ref_rgb.r-ref_tolerance.r*multiplier))
                //check g value
                if( rgb_img[x_1][y_1].g <= (ref_rgb.g+ref_tolerance.g) && rgb_img[x_1][y_1].g >= (ref_rgb.g-ref_tolerance.g))
                    {
                    //check b value
                    if( rgb_img[x_1][y_1].b <= (ref_rgb.b+ref_tolerance.b) && rgb_img[x_1][y_1].b >= (ref_rgb.b-ref_tolerance.b))
                        bool_img[x_1][y_1] = 1;
                    }
                }


            //std::cout << rgb_img[x_1][y_1].r << " " << (ref_rgb.r+ref_tolerance.r) << " " << rgb_img[x_1][y_1].r << " " << ref_rgb.r << " " << ref_tolerance.r;
           // if(bool_img[x_1][y_1] == 1)
               // std::cout << bool_img[x_1][y_1];
        }
    }


    std::cout << "Init pass completed." << std::endl;
}

void bool_sec_pass()
{
    for( int x_1 = 1; x_1 < (w_tot-1); x_1++)
    {
        for( int y_1 = 1; y_1 < (h_tot-1); y_1++)
        {
            //check adjacency
            if( bool_img[x_1+1][y_1] == 1 || bool_img[x_1-1][y_1] == 1 || bool_img[x_1][y_1+1] == 1 || bool_img[x_1][y_1-1] == 1 )
            {
                //check the rgb threshold with multipliers
                if( rgb_img[x_1][y_1].r <= (ref_rgb.r+ref_tolerance.r*multiplier) && rgb_img[x_1][y_1].r >= (ref_rgb.r-ref_tolerance.r*multiplier))
                {
                //if(rgb_img[x_1-1][y_1-1].r <= (ref_rgb.r+ref_tolerance.r*multiplier) && rgb_img[x_1-1][y_1-1].r >= (ref_rgb.r-ref_tolerance.r*multiplier))
                //check g value
                if( rgb_img[x_1][y_1].g <= (ref_rgb.g+ref_tolerance.g*multiplier) && rgb_img[x_1][y_1].g >= (ref_rgb.g-ref_tolerance.g*multiplier))
                    {
                    //check b value
                    if( rgb_img[x_1][y_1].b <= (ref_rgb.b+ref_tolerance.b*multiplier) && rgb_img[x_1][y_1].b >= (ref_rgb.b-ref_tolerance.b*multiplier))
                        bool_img[x_1][y_1] = 1;
                    }
                }
            }
        }
    }
    std::cout << "Secondary pass completed." << std::endl;
}


void draw_screen(px_color arr[4271][2848])
{

    //mark channel as empty/not displayed by using channel 3
    std::cout << "drawing...";

    HDC hdc=GetDC(sHwnd);
    for(int x = 0; x < 4271; x++)
        for(int y = 0; y < 2848; y++)
            SetPixel(hdc, x, y, RGB(abs(arr[x][y].r),abs(arr[x][y].g),abs(arr[x][y].b)));
    ReleaseDC(sHwnd,hdc);

    std::cout << "done" << std::endl;
}

void draw_bool(bool arr[4271][2848])
{

    //mark channel as empty/not displayed by using channel 3
    std::cout << "drawing...";

    HDC hdc=GetDC(sHwnd);
    for(int x = 0; x < 4271; x++)
        for(int y = 0; y < 2848; y++)
            SetPixel(hdc, x, y, RGB(arr[x][y]*255,arr[x][y]*255,arr[x][y]*255));
    ReleaseDC(sHwnd,hdc);

    std::cout << "done" << std::endl;
}

std::string str_line( int line)
{
    //turns a row of bool values into a single line of csv file
    std::string l;
    for(int i = 0; i < w_tot; i++)
    {
        l.append(1, bool_img[line][i] ? '1' : '0');
        l.append(", ");
    }
    return l;
}

void save_csv( std::string filename )
{
    //writes the boolean csv table line by line with lines from str_line
      std::ofstream myfile;
      myfile.open (filename);
      for( int a = 0; a < h_tot; a++ )
      {
          myfile << str_line(a);
          myfile << " \n";
      }
      myfile.close();

      std::cout << "Data saved to .csv" << std::endl;
}

void main_loop( char* import_name, std::string export_name )
{
    //pretty much just a compressed form of the main contents
    load_BMP( import_name );

    //run the actual cutoff
    bool_init_pass();
    for(int z = 0; z < 10; z++)
        bool_sec_pass();

    str_line(0);
    save_csv( export_name );

    //draw_screen(rgb_img);
    //draw_bool(bool_img);
}

void batch_process( int no_of_files )
{
    std::string import_names[20];
    std::string export_names[20];

    std::string prefix = "G";
    std::string format_1 = ".bmp";
    std::string format_2 = ".csv";

    //create 2 lists of exact filenames to read and write
    //WARNING: no safety checks, if you f up, it may be dangerous, overwrite something, memory leak, etc
    for( int i = 0; i < no_of_files; i++ )
    {
        import_names[i] = prefix + std::to_string(i+1) + format_1;
        export_names[i] = prefix + std::to_string(i+1) + format_2;
    }

    //actually carry out the main loop for each file
    for( int j = 0; j < no_of_files; j++ )
    {
        std::string str;
        str = import_names[j];
        char * writable = new char[str.size() + 1];
        std::copy(str.begin(), str.end(), writable);
        writable[str.size()] = '\0';

        main_loop( writable, export_names[j] );
    }
}

int main()
{
    //number of files to process
    batch_process( 1 );

    return 0;
}
