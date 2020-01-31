// -*- coding:utf-8-unix; mode:c; -*-
// Kinto x11 command line
/*
  Reference material
  get the active window on X window system
  http://k-ui.jp/blog/2012/05/07/get-active-window-on-x-window-system/
 */
// To compile
// gcc kintox11.c -lX11 -lXmu -ljson-c
//
//

#include <stdlib.h>
#include <stdio.h>
#include <locale.h>
#include <string.h>
#include <ctype.h>
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

  FILE *fp;
  char buffer[10240];
  struct json_object *parsed_json, *config, *config_obj, 
  *config_obj_name, *config_obj_run, *config_obj_de, 
  *config_obj_appnames, *appnames_obj, *init, *de, 
  *de_obj, *de_obj_id, *de_obj_active, *de_obj_run;

  int arraylen;
  int appnames_len, init_len, de_len, config_de_len;
  int system(const char *command);

  size_t i,n,r; 

  fp = fopen("kinto.json","r");
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

  // Grab all de variable info needed
  for (i = 0; i < de_len; i++) {
    de_obj = json_object_array_get_idx(de, i);
    de_obj_id = json_object_object_get(de_obj, "id");
    de_id_array[i] = json_object_get_int(de_obj_id);
    de_obj_active = json_object_object_get(de_obj, "active");
    de_active_array[i] = json_object_get_int(de_obj_active);
    de_obj_run = json_object_object_get(de_obj, "run");
    de_run_array[i] = json_object_get_string(de_obj_run);
    printf("de_run_array[%ld]: %s\n",i,de_run_array[i]);
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
        // printf("%s i:%ld n:%ld %s\n",name_array[i],i,n,appnames_array[i][n]);
      }
    }
    if(appnames_max > appnames_len){
      for (n = appnames_len; n < appnames_max; n++){
        appnames_array[i][n] = NULL;
        // printf("%s i:%ld n:%ld %s\n",name_array[i],i,n,appnames_array[i][n]);
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

  for (i = 0; i < init_len; i++) {
    init_array[i] = json_object_get_int(json_object_array_get_idx(init, i));
    int de_id_idx = in_int(de_id_array, de_len, init_array[i]);
    printf("Running init command: %s\n",de_run_array[de_id_idx]);
    system(de_run_array[de_id_idx]);
  }

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

  int breakouter;

  for (;;)
  {
    breakouter = 0;

    if(strcmp(str_window_class(d, w,prior_app),prior_app)){
      for(i = 0; i < arraylen; ++i){
        if(breakouter == 0){
          if(strcmp(name_array[i],"gui")){
            for(n = 0; n < appnames_max; ++n){
              if (appnames_array[i][n] != NULL){
                // printf("%s\n",appnames_array[i][n]);
                // If statement for triggering terminal config
                if((strcicmp(appnames_array[i][n], str_window_class(d, w,prior_app)) == 0 && (remap_bool == 1 || remap_bool == 2))) {
                  // printf("1st if %s i:%ld n:%ld %s\n",name_array[i],i,n,appnames_array[i][n]);
                  printf("%s\n",name_array[i]);
                  system(run_array[i]);
                  for(r = 0; r < config_de_max; r++){
                    if(config_de_array[i][r] != -1){
                      int de_id_idx = in_int(de_id_array, de_len, config_de_array[i][r]);
                      // printf("Running de command: %s\n",de_run_array[de_id_idx]);
                      system(de_run_array[de_id_idx]);
                    }
                  }
                  remap_bool = 0;
                  fflush(stdout);
                  breakouter = 1;
                  break;
                } // Else command for ignoring similar app category based on config
                else if((strcicmp(appnames_array[i][n], str_window_class(d, w,prior_app)) == 0 && remap_bool == 0)){
                  // printf("2nd elseif %s i:%ld n:%ld %s\n",name_array[i],i,n,appnames_array[i][n]);
                  breakouter = 1;
                  break;
                } // Else command for triggering gui config
                else if ((i == arraylen-1 || appnames_array[i][n+1] == NULL) && (remap_bool == 0 || remap_bool == 2)){
                  char *find = "gui";
                  int gui_idx = in(name_array, arraylen, find);

                  if(gui_idx >= 0) {
                    printf("%s\n",name_array[gui_idx]);
                    system(run_array[gui_idx]);
                  }
                  for(r = 0; r < config_de_max; r++){
                    if(config_de_array[gui_idx][r] != -1){
                      int de_id_idx = in_int(de_id_array, de_len, config_de_array[gui_idx][r]);
                      // printf("Running de command: %s\n",de_run_array[de_id_idx]);
                      system(de_run_array[de_id_idx]);
                    }
                  }
                  // printf("3rd elseif %s i:%ld n:%ld %s\n",name_array[i],i,n,appnames_array[i][n]);
                  remap_bool = 1;
                  fflush(stdout);
                  breakouter = 1;
                  break;
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
    strcpy(prior_app,str_window_class(d, w, prior_app));

    XEvent e;
    XNextEvent(d, &e);
    w = get_focus_window(d);

  }
}