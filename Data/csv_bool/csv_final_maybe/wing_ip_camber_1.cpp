#include <iostream>
#include <string>
#include <algorithm>
#include <windows.h>
#include <cmath>
#include <fstream>
#include <filesystem>


//global variables

//image size init (later read from the bmp header)
int w_tot = 0;
int h_tot = 0;
//printing thing
static HWND sHwnd;
//struct for rgb data
struct px_color
{
    int r;
    int g;
    int b;
};
//rgb image storage
px_color rgb_img[4272][2848];
//processed bool image storage
bool bool_img[4272][2848];
bool camber_img[4272][2848];
//reference color for pixel seeking
px_color ref_rgb = {230, 101, 43};
//default tolerance and multiplier for them
px_color ref_tolerance = {5, 5, 5};
float multiplier = 15;

//storage for point locations and the associated gradients
struct point_data
{
    //location, ver is fixed based on spacing
    int loc_ver;
    int loc_hor;
    //both intercept locations, horizontal
    int p1;
    int p2;
    //lenght from p1 to p2, pytagorean
    int span;
    //gradient (max value if vertical)
    float grad;
};
//actual storage array
//static array, so max 500 points scanned
point_data camber_points[500];
//scaling factor for printing
const int scaled_res = 500;

void refresh_scr()
{
    HDC hdc=GetDC(sHwnd);
    for(int x = 0; x < scaled_res; x = x+2)
        for(int y = 0; y < scaled_res; y = y+2)
            SetPixel(hdc, x, y, RGB((x*y)/(scaled_res),x/scaled_res,y*scaled_res));
    for(int x = 0; x < scaled_res; x = x+1)
        for(int y = 0; y < scaled_res; y = y+1)
            SetPixel(hdc, x, y, RGB(0,0,0));
    ReleaseDC(sHwnd,hdc);
}

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
    //std::cout << "Secondary pass completed." << std::endl;
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

std::string str_line_camber( int line)
{
    //turns a row of bool values into a single line of csv file
    std::string l;
    for(int i = 0; i < w_tot; i++)
    {
        l.append(1, camber_img[line][i] ? '1' : '0');
        //std::cout << "ab ";
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

void save_csv_camber( std::string filename )
{
    //writes the boolean csv table line by line with lines from str_line
      std::ofstream myfile;
      myfile.open (filename);
      for( int a = 0; a < h_tot; a++ )
      {
          myfile << str_line_camber(a);
          //std::cout << str_line_camber(a);
          myfile << " \n";
      }
      myfile.close();

    for( int x_1 = 0; x_1 < w_tot; x_1++)
        {
            for( int y_1 = 0; y_1 < h_tot; y_1++)
            {
                camber_img[x_1][y_1] = 0;
            }
        }

      std::cout << "Data saved to .csv" << std::endl;
}

//=======================================
//FINDING THE CAMBERLINE STARTS HERE
//=======================================
void define_scanlines_vert( int no_of_lines )
{
    //just define the vertical locations of each scanline and their spacing
    int spacing = int(h_tot/no_of_lines);

    for( int i = 0; i <= no_of_lines; i++ )
    {
        camber_points[i].loc_ver = i*spacing;
        //std::cout << i << " " << i*spacing << std::endl;
    }
}

void scan_hor(int no_of_lines )
{
    int tmp1 = 0;
    int tmp2 = 0;
    //loop thru the lines to scan
    for( int i = 0; i < no_of_lines; i++ )
    {
        //reset in case all conditions werent passed in the last line
        tmp1 = 0;
        tmp2 = 0;
        //loop through the line
        for( int j = 0; j < w_tot; j++ )
        {
            //find the first (outer) intercept
            if( bool_img[ camber_points[i].loc_ver ][j] == 1  && tmp1 != 2 )
            {
                tmp1 = 1;
                tmp2 = j;
            }
            //find the first (inner) intercept (p1)
            if( tmp1 == 1 )
                if( bool_img[ camber_points[i].loc_ver ][j] == 0 )
                {
                    camber_points[i].p1 = tmp2;
                    tmp1 = 2;
                }
            //find the second (inner) intercept (p2)
            if( tmp1 == 2 )
                if( bool_img[ camber_points[i].loc_ver ][j] == 1 )
                {
                    camber_points[i].p2 = j;
                }
        }

        //find span and midpoint
        if( camber_points[i].p1 != 0 && camber_points[i].p2 != 0 )
        {
            camber_points[i].span = camber_points[i].p2 - camber_points[i].p1;
            camber_points[i].loc_hor = camber_points[i].p1 + camber_points[i].span/2;

            //test draw
            camber_img[ camber_points[i].loc_ver ][ camber_points[i].loc_hor ] = 1;
            //std::cout << "dupa dupa";
        }
        else
            camber_img[ camber_points[i].loc_ver ][ camber_points[i].loc_hor ] = 0;

        //std::cout << i+1 << " " << camber_points[i].p1 << " " << camber_points[i].p2 << " " << camber_points[i].loc_hor << std::endl;
    }
}


void scale_and_print_bool( bool arr1[4272][2848])
{
    bool bool_img2[scaled_res][scaled_res];

    for( int x_1 = 0; x_1 < scaled_res; x_1++)
        {
            for( int y_1 = 0; y_1 < scaled_res; y_1++)
            {
                bool_img2[x_1][y_1] = 0;
            }
        }
    //shitty bootleg scaler
    for( int i = 0; i < h_tot; i++ )
        for( int j = 0; j < w_tot; j++ )
        {
            if( arr1[i][j] == 1)
                bool_img2[int(float(i)*(float(scaled_res)/float(h_tot)))][int(float(j)*(float(scaled_res)/float(w_tot)))] = 1;
                //std::cout << int(float(i)*(500.0/float(h_tot))) << " " << int(float(j)*(500.0/float(w_tot))) << std::endl;
        }

    HDC hdc=GetDC(sHwnd);
    for(int x = 0; x < scaled_res; x++)
        for(int y = 0; y < scaled_res; y++)
            if( bool_img2[x][y] == 1 )
                SetPixel(hdc, x, y, RGB(bool_img2[x][y]*255,bool_img2[x][y]*255,bool_img2[x][y]*255));
    ReleaseDC(sHwnd,hdc);

    for( int x_1 = 0; x_1 < w_tot; x_1++)
    {
        for( int y_1 = 0; y_1 < h_tot; y_1++)
        {
            arr1[x_1][y_1] == 0;
        }
    }

}

void find_gradients( int w )
{
    //this function finds approximate gradient at each camberline point
    for( int i = 0; i < 499; i++ )
    {
        //check if there is even a camber point with such number
        if( camber_points[i].loc_hor != 0 && camber_points[i+1].loc_hor != 0 )
        {
            if( (i == 0 || camber_points[i+1].loc_hor != 0) && camber_points[i].loc_hor != 0 && camber_points[i-1].loc_hor == 0 )
            {
                //find gradient if it is the first point after any discontinuity
                int tmp1 = camber_points[i+1].loc_hor - camber_points[i].loc_hor;
                int tmp2 = camber_points[i+1].loc_ver - camber_points[i].loc_ver;
                camber_points[i].grad = float(tmp1)/float(tmp2);
            }
            if( (i == 499 || camber_points[i-1].loc_hor != 0) && camber_points[i].loc_hor != 0 && camber_points[i+1].loc_hor == 0 )
            {
                //find gradient if it is the last point before any discontinuity
                int tmp1 = camber_points[i].loc_hor - camber_points[i-1].loc_hor;
                int tmp2 = camber_points[i].loc_ver - camber_points[i-1].loc_ver;
                camber_points[i].grad = float(tmp1)/float(tmp2);
            }
            if( i != 0 && i != 499 && camber_points[i-1].loc_hor != 0 && camber_points[i].loc_hor != 0 && camber_points[i+1].loc_hor != 0 )
            {
                //find gradient if it is the middle of normal and sane continous section
                int tmp1 = camber_points[i+1].loc_hor - camber_points[i-1].loc_hor;
                int tmp2 = camber_points[i+1].loc_ver - camber_points[i-1].loc_ver;
                camber_points[i].grad = float(tmp1)/float(tmp2);
            }
        }
        if( camber_points[i].loc_hor != 0 )
        {
           // std::cout << i << " " << camber_points[i].grad << std::endl;
           // std::cout << camber_points[i-1].loc_hor << " " << camber_points[i].loc_hor << " " << camber_points[i+1].loc_hor << std::endl;
           // std::cout << camber_points[i-1].loc_ver << " " << camber_points[i].loc_ver << " " << camber_points[i+1].loc_ver << std::endl;
           // std::cout << std::endl;
        }
    }

    //writes the boolean csv table line by line PLACEHOLDER DUMP OF CAMBER DATA
      std::ofstream myfile;
      std::string filename_camber = "placeholder_camber_dump.csv";
      myfile.open ( filename_camber );
      for( int a = 0; a < w; a++ )
      {
          std::string l;
          //l.append(a, ", ", camber_points[a].loc_hor, ", ", camber_points[a].loc_ver, ", ", camber_points[a].grad );
          l += std::to_string(a);
          l += (", ");
          l += std::to_string(camber_points[a].loc_hor);
          l += (", ");
          l += std::to_string(camber_points[a].loc_ver);
          l += (", ");
          l += std::to_string(camber_points[a].grad);

          myfile << l;
          myfile << " \n";
      }
      myfile.close();
}


void main_loop( char* import_name, std::string export_name, std::string export_name2, int fx, int flag2 )
{
    //pretty much just a compressed form of the main contents
    if(std::filesystem::exists(import_name))
        load_BMP( import_name );

    //run the actual cutoff
    bool_init_pass();
    for(int z = 0; z < 500; z++)
    {
        bool_sec_pass();
        //std::cout << "Secondary pass No." << fx << "." << z+1 << " completed." << std::endl;
    }

    if( flag2 == 1 )
        refresh_scr();
        scale_and_print_bool( bool_img );

    str_line(0);

    int magic_variable = 300;
    define_scanlines_vert( magic_variable );
    scan_hor( magic_variable );

    save_csv( export_name );

    if( flag2 == 1 )
        scale_and_print_bool( camber_img );

    save_csv_camber( export_name2 );

    //draw_screen(rgb_img);
    //draw_bool(bool_img);
}

void batch_process( int no_of_files, int flag1 )
{
    std::string import_names[20];
    std::string export_names[20];
    std::string export_names2[20];

    std::string prefix = "G";
    std::string suffix = "camber";
    std::string format_1 = ".bmp";
    std::string format_2 = ".csv";

    //create 2 lists of exact filenames to read and write
    //WARNING: no safety checks, if you f up, it may be dangerous, overwrite something, memory leak, etc
    for( int i = 0; i < no_of_files; i++ )
    {
        import_names[i] = prefix + std::to_string(i+1) + format_1;
        export_names[i] = prefix + std::to_string(i+1) + format_2;
        export_names2[i] = prefix + std::to_string(i+1) + suffix + format_2;
    }

    //actually carry out the main loop for each file
    for( int j = 0; j < no_of_files; j++ )
    {
        std::string str;
        str = import_names[j];
        char * writable = new char[str.size() + 1];
        std::copy(str.begin(), str.end(), writable);
        writable[str.size()] = '\0';

        for( int x_1 = 0; x_1 < w_tot; x_1++)
        {
            for( int y_1 = 0; y_1 < h_tot; y_1++)
            {
                bool_img[x_1][y_1] = 0;
                camber_img[x_1][y_1] = 0;
            }
        }

        std::cout<< std::endl <<"Processing image No." << j << std::endl;

        main_loop( writable, export_names[j], export_names2[j], j+1, flag1 );
    }
}



int main()
{
    //number of files to process
    //2nd is a flag to print, first is number of images to process
    batch_process( 20, 1 );
    //draw_bool(bool_img);
    find_gradients( 300 );

    return 0;
}
