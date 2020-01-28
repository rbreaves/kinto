// -*- coding:utf-8-unix; mode:c; -*-
// Kinto x11 command line
/*
  Reference material
  get the active window on X window system
  http://k-ui.jp/blog/2012/05/07/get-active-window-on-x-window-system/
 */
// To compile
// gcc active_window.c -lX11 -lXmu
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

// get the top window.
// a top window have the following specifications.
//  * the start window is contained the descendent windows.
//  * the parent window is the root window.
Window get_top_window(Display* d, Window start){
  Window w = start;
  Window parent = start;
  Window root = None;
  Window *children;
  unsigned int nchildren;
  Status s;

  while (parent != root) {
    w = parent;
    s = XQueryTree(d, w, &root, &parent, &children, &nchildren); // see man

    if (s)
      XFree(children);

    if(xerror){
      printf("failed to get top window\n");
      exit(1);
    }
  }

  return w;
}

// search a named window (that has a WM_STATE prop)
// on the descendent windows of the argment Window.
Window get_named_window(Display* d, Window start){
  Window w;
  w = XmuClientWindow(d, start); // see man
  if(w == start)
  return w;
}

// (XFetchName cannot get a name with multi-byte chars)
void print_window_name(Display* d, Window w){
  XTextProperty prop;
  Status s;

  s = XGetWMName(d, w, &prop); // see man
  if(!xerror && s){
    int count = 0, result;
    char **list = NULL;
    result = XmbTextPropertyToTextList(d, &prop, &list, &count); // see man
    if(result == Success){
      printf("\t%s\n", list[0]);
    }else{
      // printf("ERROR: XmbTextPropertyToTextList\n");
    }
  }else{
    // printf("ERROR: XGetWMName\n");
  }
}

void print_window_class(Display* d, Window w){
  Status s;
  XClassHint* class;

  class = XAllocClassHint(); // see man
  if(xerror){
    // printf("ERROR: XAllocClassHint\n");
  }

  s = XGetClassHint(d, w, class); // see man
  if(xerror || s){
    // printf("\tname: %s\n\tclass: %s\n", class->res_name, class->res_class);
    printf("%s\n", class->res_class);
  }else{
    printf("ERROR: XGetClassHint\n");
  }
}

const char * str_window_class(Display* d, Window w){
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
    char * error_msg;
    error_msg = malloc(sizeof(char)*50);
    strcpy(error_msg, "ERROR: XGetClassHint");
    return error_msg;
  }
}

void print_window_info(Display* d, Window w){
  print_window_class(d, w);
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

  // printf("\n The content of the file %s  are : \n","./appnames.csv");    
  // for(i = 0; i < tot; ++i)
  // {
  //     printf("%s\n", line[i]);
  // }
  // printf("\n");

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
  w = get_top_window(d, w);
  w = get_named_window(d, w);

  for (;;)
  {

    if(strcmp(str_window_class(d, w),prior_app)){
      int len = sizeof(line)/sizeof(line[0]);
      // printf("length: %d\n",len);
      int i;
      for(i = 0; i < len; ++i){
        // printf("i: %d\n",i);
        // printf(strcicmp(line[i], str_window_class(d, w)));
        if((strcicmp(line[i], str_window_class(d, w)) == 0 && (remap_bool == 1 || remap_bool == 2))) {
            // printf("Gotcha!\n");
            // printf("%s - prior app %s\n",str_window_class(d, w),prior_app);
            printf("%s\n","term");
            remap_bool = 0;
            fflush(stdout);
            break;
        }
        else if((strcicmp(line[i], str_window_class(d, w)) == 0 && remap_bool == 0)){
          break;
        }
        else if (i == 49 && (remap_bool == 0 || remap_bool == 2)){
          printf("%s\n","gui");
          // printf("no match - %s - prior app %s\n",str_window_class(d, w),prior_app);
          remap_bool = 1;
          fflush(stdout);
          break;
        }
      }
    }
    strcpy(prior_app,str_window_class(d, w));

    XEvent e;
    XNextEvent(d, &e);
    // get active window
    w = get_focus_window(d);
    w = get_top_window(d, w);
    w = get_named_window(d, w);
  }
}