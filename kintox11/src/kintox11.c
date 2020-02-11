// -*- coding:utf-8-unix; mode:c; -*-
// Kinto x11 command line
/*
  Reference material
  get the active window on X window system
  http://k-ui.jp/blog/2012/05/07/get-active-window-on-x-window-system/
 */
// To compile without static libraries
// gcc kintox11.c -lX11 -lXmu -ljson-c
//
// To compile with static library json-c 
// Make sure archive with object files exist ar -t /usr/local/lib/libjson-c.a
// gcc -L/usr/local/lib/ kintox11.c -ljson-c -lXmu -lXt -lX11 -O2 -o kintox11
//

#include <stdlib.h>
#include <stdio.h>
#include <locale.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <X11/Xlib.h>           // `apt-get install libx11-dev`
#include <X11/Xmu/WinUtil.h>    // `apt-get install libxmu-dev`
#include <json-c/json.h>        // `apt install libjson-c-dev`

Bool xerror = False;

int in_int(int a[],int size,int item) 
{ 
    int i,pos=-1; 
    for(i=0;i< size;i++) 
    { 
        if(a[i]==item) 
        { 
            pos=i; 
            break; 
        } 
    } 
    return pos; 
} 

int in(const char **arr, int len, char *target) {
  int i;
  for(i = 0; i < len; i++) {
    if(strncmp(arr[i], target, strlen(target)) == 0) {
      return i;
    }
  }
  return -1;
}

int strcicmp(char const *a, char const *b)
{
    for (;; a++, b++) {
        int d = tolower((unsigned char)*a) - tolower((unsigned char)*b);
        if (d != 0 || !*a)
            return d;
    }
}

Display* open_display(){
  int i;
  Display* d = XOpenDisplay(NULL);
  for (i = 0; i < 60; i++) {
    if(d == NULL){
      printf("fail to open X server display...\n");
    }
    else{
      break;
    }
    sleep(1);
  }
  if(d == NULL){
    printf("fail to open X server display for 1 minute...\n");
    printf("Kintox11 is now exiting...\n");
    exit(1);
  }
  return d;
}

int handle_error(Display* display, XErrorEvent* error){
  printf("X11 error: type=%d, serial=%lu, code=%d\n",
    error->type, error->serial, (int)error->error_code);
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

  while (parent != root && parent != 0) {
    w = parent;
    s = XQueryTree(d, w, &root, &parent, &children, &nchildren); // see man

    if (s)
      XFree(children);

    if(xerror){
      printf("fail to get top window: %ld\n",w);
      exit(1);
    }

    // printf("  get parent (window: %d)\n", (int)w);
  }

  // printf("success (window: %d)\n", (int)w);

  return w;
}

// search a named window (that has a WM_STATE prop)
// on the descendent windows of the argment Window.
Window get_named_window(Display* d, Window start){
  Window w;
  // printf("getting named window ... ");
  w = XmuClientWindow(d, start); // see man
  // if(w == start)
  //   printf("fail\n");
  // printf("success (window: %d)\n", (int) w);
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

  FILE *fp;
  char buffer[10240];
  struct json_object *parsed_json, *config, *config_obj, 
  *config_obj_name, *config_obj_run, *config_obj_de, 
  *config_obj_appnames, *appnames_obj, *init, *de, 
  *de_obj, *de_obj_id, *de_obj_active, *de_obj_run,
  *de_obj_runterm,*de_obj_rungui;

  int arraylen;
  int appnames_len, init_len, de_len, config_de_len;
  int system(const char *command);

  size_t i,n,r; 
  
  printf("Importing user_config.json...\n");
  fp = fopen("user_config.json","r");
  fread(buffer, 10240, 1, fp);
  fclose(fp);

  parsed_json = json_tokener_parse(buffer);

  config = json_object_object_get(parsed_json, "config");
  init = json_object_object_get(parsed_json, "init");
  de = json_object_object_get(parsed_json, "de");

  arraylen = json_object_array_length(config);
  init_len = json_object_array_length(init);
  de_len = json_object_array_length(de);

  const char *name_array[arraylen];
  const char *run_array[arraylen];
  int init_array[init_len];

  int de_id_array[de_len];
  Bool de_active_array[de_len];
  const char *de_run_array[de_len];
  const char *de_runterm_array[de_len];
  const char *de_rungui_array[de_len];

  // Grab all de variable info needed
  for (i = 0; i < de_len; i++) {
    de_obj = json_object_array_get_idx(de, i);
    de_obj_id = json_object_object_get(de_obj, "id");
    de_id_array[i] = json_object_get_int(de_obj_id);
    de_obj_active = json_object_object_get(de_obj, "active");
    de_active_array[i] = json_object_get_int(de_obj_active);
    de_obj_run = json_object_object_get(de_obj, "run");
    de_run_array[i] = json_object_get_string(de_obj_run);
    de_obj_runterm = json_object_object_get(de_obj, "run_term");
    de_runterm_array[i] = json_object_get_string(de_obj_runterm);
    de_obj_rungui = json_object_object_get(de_obj, "run_gui");
    de_rungui_array[i] = json_object_get_string(de_obj_rungui);
    // printf("de_run_array[%ld]: %s\n",i,de_run_array[i]);
  }
  // de ends

  int appnames_max = 0;
  int config_de_max = 0;

  for (i = 0; i < arraylen; i++) {
    config_obj = json_object_array_get_idx(config, i);
    config_obj_appnames = json_object_object_get(config_obj, "appnames");
    config_obj_de = json_object_object_get(config_obj, "de");

    appnames_len = json_object_array_length(config_obj_appnames);
    if (appnames_len > appnames_max){
      appnames_max = appnames_len;
    }
    config_de_len = json_object_array_length(config_obj_de);
    if(config_de_len > config_de_max){
      config_de_max = config_de_len;
    }
  }

  const char *appnames_array[arraylen][appnames_max];
  int config_de_array[arraylen][config_de_max];

  for (i = 0; i < arraylen; i++) {
    config_obj = json_object_array_get_idx(config, i);
    config_obj_name = json_object_object_get(config_obj, "name");
    config_obj_run = json_object_object_get(config_obj, "run");
    name_array[i] = json_object_get_string(config_obj_name);
    run_array[i] = json_object_get_string(config_obj_run);
    // printf("%s\n%s\n", json_object_get_string(config_obj_name), json_object_get_string(config_obj_run));

    config_obj_appnames = json_object_object_get(config_obj, "appnames");
    appnames_len = json_object_array_length(config_obj_appnames);
    for (n = 0; n < appnames_len; n++) {
      // printf("name_array[i]: %s\n",name_array[i]);
      if(!strcicmp(name_array[i], "gui")){
        appnames_array[i][n] = NULL;
        // printf("%s i:%ld n:%ld %s\n",name_array[i],i,n,appnames_array[i][n]);
      }
      else{
        appnames_array[i][n] = json_object_get_string(json_object_array_get_idx(config_obj_appnames, n));
        //printf("%s i:%ld n:%ld %s\n",name_array[i],i,n,appnames_array[i][n]);
      }
    }
    if(appnames_max > appnames_len){
      for (n = appnames_len; n < appnames_max; n++){
        appnames_array[i][n] = NULL;
        //printf("%s i:%ld n:%ld %s\n",name_array[i],i,n,appnames_array[i][n]);
      }
    }

    config_obj_de = json_object_object_get(config_obj, "de");
    config_de_len = json_object_array_length(config_obj_de);
    for (n = 0; n < config_de_max; n++) {
      if(n < config_de_len){
        // printf("de value: %d\n",json_object_get_int(json_object_array_get_idx(config_obj_de, n)));
        config_de_array[i][n] = json_object_get_int(json_object_array_get_idx(config_obj_de, n));
      }
      else{
        // printf("de -1 value: %d\n",json_object_get_int(json_object_array_get_idx(config_obj_de, n)));
        config_de_array[i][n] = -1;
      }

    }
  }
  
  printf("Data from user_config.json imported successfully.\n");

  for (i = 0; i < init_len; i++) {
    init_array[i] = json_object_get_int(json_object_array_get_idx(init, i));
    int de_id_idx = in_int(de_id_array, de_len, init_array[i]);
    printf("Running init command: %s\n",de_run_array[de_id_idx]);
    system(de_run_array[de_id_idx]);
  }

  Display* d;
  Window w;
  char *name;

  // for XmbTextPropertyToTextList
  setlocale(LC_ALL, ""); // see man locale

  d = open_display();
  XSelectInput(d, DefaultRootWindow(d), SubstructureNotifyMask);
  XSetErrorHandler(handle_error);

  char * prior_app;
  char * current_app;
  prior_app = malloc(sizeof(char)*100);
  strcpy(prior_app,"none");

  int remap_bool = 2;

  printf("Starting keyswap...\n");

  // get active window
  w = get_focus_window(d);
  w = get_top_window(d, w);
  w = get_named_window(d, w);

  // XFetchName(d, w, &name);
  // printf("window:%#x name:%s\n", w, name);
  printf("First window name: %s \n",str_window_class(d, w,prior_app));

  int breakouter;

  for (;;)
  {
    current_app = str_window_class(d, w,prior_app);
    breakouter = 0;
    // XFetchName(d, w, &name);
    // printf("window:%#x name:%s\n", w, name);
    // printf("%s\n","1");
    // printf("%s\n",str_window_class(d, w,prior_app));
    if(strcmp(current_app,prior_app) || !strcmp(current_app,"none")){
      // printf("%s\n","2");
      for(i = 0; i < arraylen; ++i){
        if(breakouter == 0){
          if(strcmp(name_array[i],"gui")){
            // printf("%s\n","3");
            for(n = 0; n < appnames_max; ++n){
              // printf("2nd elseif %s i:%ld n:%ld %s\n",name_array[i],i,n,appnames_array[i][n]);
              // printf("3rd elseif (i:%ld == arraylen-1:%d && appnames_array[i:%ld][n:%ld+1]:%s  == NULL) && (remap_bool: %i == 0 || 2)\n",i,arraylen-1,i,n,appnames_array[i][n+1],remap_bool);
              if (appnames_array[i][n] != NULL){
                // printf("%s\n",appnames_array[i][n]);
                // If statement for triggering terminal config
                if((strcicmp(appnames_array[i][n], current_app) == 0 && (remap_bool == 1 || remap_bool == 2))) {
                  // printf("1st if %s i:%ld n:%ld %s\n",name_array[i],i,n,appnames_array[i][n]);
                  printf("%s: %s\n",name_array[i],current_app);
                  system(run_array[i]);
                  for(r = 0; r < config_de_max; r++){
                    if(config_de_array[i][r] != -1){
                      int de_id_idx = in_int(de_id_array, de_len, config_de_array[i][r]);
                      // printf("Running de command: %s\n",de_run_array[de_id_idx]);
                      system(de_runterm_array[de_id_idx]);
                    }
                  }
                  remap_bool = 0;
                  fflush(stdout);
                  breakouter = 1;
                  break;
                } // Else command for ignoring similar app category based on config
                else if((strcicmp(appnames_array[i][n], current_app) == 0 && remap_bool == 0)){
                  printf("    %s\n",current_app);
                  // printf("in 2nd elseif %s i:%ld n:%ld %s\n",name_array[i],i,n,appnames_array[i][n]);
                  // printf("%s\n","4");
                  breakouter = 1;
                  break;
                } // Else command for triggering gui config
                else if ((i == arraylen-1 && (appnames_array[i][n] == NULL || appnames_max == n+1)) && (remap_bool == 0 || remap_bool == 2)){
                  // printf("in 3rd elseif (i:%ld == arraylen-1:%d && appnames_array[i:%ld][n:%ld+1]:%s  == NULL) && (remap_bool: %i == 0 || 2)\n",i,arraylen-1,i,n,appnames_array[i][n+1],remap_bool);
                  char *find = "gui";
                  int gui_idx = in(name_array, arraylen, find);

                  if(gui_idx >= 0) {
                    printf("%s: %s\n",name_array[gui_idx],current_app);
                    system(run_array[gui_idx]);
                  }
                  for(r = 0; r < config_de_max; r++){
                    if(config_de_array[gui_idx][r] != -1){
                      int de_id_idx = in_int(de_id_array, de_len, config_de_array[gui_idx][r]);
                      // printf("Running de command: %s\n",de_run_array[de_id_idx]);
                      system(de_rungui_array[de_id_idx]);
                    }
                  }
                  
                  remap_bool = 1;
                  fflush(stdout);
                  breakouter = 1;
                  break;
                } // GUI app still - no switching needed
                else if ((i == arraylen-1 && appnames_max == n+1) && remap_bool == 1){
                  printf("    %s\n",current_app);
                }
                else if ((i == arraylen-1 && appnames_max == n+1)){
                  printf("%s - Failed to match any keyswap requirements\n",current_app);
                }
              }
            }
          }
        }
        else{
          break;
        }
      }
    }
    // printf("%s\n","5");
    strcpy(prior_app,str_window_class(d, w, prior_app));

    XEvent e;
    XNextEvent(d, &e);
    w = get_focus_window(d);
    w = get_top_window(d, w);
    w = get_named_window(d, w);
  }
}