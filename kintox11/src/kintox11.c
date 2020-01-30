// -*- coding:utf-8-unix; mode:c; -*-
// Kinto x11 command line
/*
  Reference material
  get the active window on X window system
  http://k-ui.jp/blog/2012/05/07/get-active-window-on-x-window-system/
 */
// To compile
// gcc kintox11.c -lX11 -lXmu
//
//

#include <stdlib.h>
#include <stdio.h>
#include <locale.h>
#include <string.h>
#include <ctype.h>
#include <X11/Xlib.h>           // `apt-get install libx11-dev`
#include <X11/Xmu/WinUtil.h>    // `apt-get install libxmu-dev`
#define LSIZ 128 // buffer
#define RSIZ 50 // array size

Bool xerror = False;

int strcicmp(char const *a, char const *b)
{
    for (;; a++, b++) {
        int d = tolower((unsigned char)*a) - tolower((unsigned char)*b);
        if (d != 0 || !*a)
            return d;
    }
}

Display* open_display(){
  Display* d = XOpenDisplay(NULL);
  if(d == NULL){
    printf("fail to open X server display...\n");
    exit(1);
  }
  return d;
}

int handle_error(Display* display, XErrorEvent* error){
  printf("ERROR: X11 error\n");
  xerror = True;
  return 1;
}

Window get_focus_window(Display* d){
  Window w;
  int revert_to;
  XGetInputFocus(d, &w, &revert_to); // see man
  if(xerror){
    printf("Error getting focused window\n");
    exit(1);
  }else if(w == None){
    printf("no focus window\n");
    exit(1);
  }

  return w;
}


const char * str_window_class(Display* d, Window w, char *prior_app ){
  Status s;
  XClassHint* class;

  class = XAllocClassHint(); // see man
  if(xerror){
    // printf("ERROR: XAllocClassHint\n");
  }

  s = XGetClassHint(d, w, class); // see man
  if(xerror || s){
    char * app_class;
    app_class = malloc(sizeof(char)*100);
    strcpy(app_class,class->res_class);
    // printf("\tname: %s\n\tclass: %s\n", class->res_name, class->res_class);
    return app_class;
  }else{
    // char * error_msg;
    // error_msg = malloc(sizeof(char)*50);
    // strcpy(error_msg, "ERROR: XGetClassHint");
    return prior_app;
  }
}

int main(void){

  char line[RSIZ][LSIZ];
  FILE *fptr = NULL; 
  int i = 0;
  int tot = 0;

  fptr = fopen("./appnames.csv", "r");
  while(fgets(line[i], LSIZ, fptr)) 
  {
      line[i][strlen(line[i])] = '\0';
      if( line[i][strlen(line[i])-1] == '\n' )
          line[i][strlen(line[i])-1] = 0;
      i++;
  }
  tot = i;

  Display* d;
  Window w;

  // for XmbTextPropertyToTextList
  setlocale(LC_ALL, ""); // see man locale

  d = open_display();
  XSelectInput(d, DefaultRootWindow(d), SubstructureNotifyMask);
  XSetErrorHandler(handle_error);

  char * prior_app;
  prior_app = malloc(sizeof(char)*100);
  strcpy(prior_app,"none");

  int remap_bool = 2;

  // get active window
  w = get_focus_window(d);

  for (;;)
  {

    if(strcmp(str_window_class(d, w,prior_app),prior_app)){
      int len = sizeof(line)/sizeof(line[0]);
      // printf("length: %d\n",len);
      int i;
      for(i = 0; i < len; ++i){
        // printf("i: %d\n",i);
        // printf(strcicmp(line[i], str_window_class(d, w, prior_app)));
        if((strcicmp(line[i], str_window_class(d, w,prior_app)) == 0 && (remap_bool == 1 || remap_bool == 2))) {
            // printf("Gotcha!\n");
            // printf("%s - prior app %s\n",str_window_class(d, w, prior_app),prior_app);
            printf("%s\n","term");
            remap_bool = 0;
            fflush(stdout);
            break;
        }
        else if((strcicmp(line[i], str_window_class(d, w,prior_app)) == 0 && remap_bool == 0)){
          break;
        }
        else if (i == 49 && (remap_bool == 0 || remap_bool == 2)){
          printf("%s\n","gui");
          // printf("no match - %s - prior app %s\n",str_window_class(d, w, prior_app),prior_app);
          remap_bool = 1;
          fflush(stdout);
          break;
        }
      }
    }
    strcpy(prior_app,str_window_class(d, w, prior_app));

    XEvent e;
    XNextEvent(d, &e);
    w = get_focus_window(d);

  }
}