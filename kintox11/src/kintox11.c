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

#define _GNU_SOURCE 1
#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <locale.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <X11/Xlib.h>           // `apt-get install libx11-dev`
#include <X11/Xmu/WinUtil.h>    // `apt-get install libxmu-dev`
#include <json-c/json.h>        // `apt install libjson-c-dev`
#include <sys/select.h>
#include <math.h>
#include <sys/time.h>
#ifdef WIN32
#include <windows.h>
#elif _POSIX_C_SOURCE >= 199309L
#include <time.h>   // for nanosleep
#else
#include <unistd.h> // for usleep
#endif

const char *eventNames[34] = {"None","KeyPress","KeyRelease","ButtonPress","ButtonRelease","MotionNotify","EnterNotify","LeaveNotify","FocusIn","FocusOut","KeymapNotify","Expose","GraphicsExpose","NoExpose","VisibilityNotify","CreateNotify","DestroyNotify","UnmapNotify","MapNotify","MapRequest","ReparentNotify","ConfigureNotify","ConfigureRequest","ResizeRequest","CirculateNotify","CirculateRequest","PropertyNotify","SelectionClear","SelectionRequest","SelectionNotify","ColormapNotify","ClientMessage","MappingNotify"};

#define NUM_THREADS 2
typedef struct threadArgs * ThreadArgs;
struct threadArgs{
  char *run_onInput;
  char *run_offInput;
};

long long timeInMilliseconds(void) {
  struct timeval tv;

  gettimeofday(&tv,NULL);
  return (((long long)tv.tv_sec)*1000)+(tv.tv_usec/1000);
}

bool debug;
bool input_check = 0;
long long int event_ts;
int last_event;

Display* d;
Window w;
XEvent e;

// cross-platform sleep function
void sleep_ms(int milliseconds) {
  #ifdef WIN32
      Sleep(milliseconds);
  #elif _POSIX_C_SOURCE >= 199309L
      struct timespec ts;
      ts.tv_sec = milliseconds / 1000;
      ts.tv_nsec = (milliseconds % 1000) * 1000000;
      nanosleep(&ts, NULL);
  #else
      usleep(milliseconds * 1000);
  #endif
}

char *trimwhitespace(char *str){
  char *end;
  // Trim leading space
  while(isspace((unsigned char)*str)) str++;
  if(*str == 0)  // All spaces?
    return str;
  // Trim trailing space
  end = str + strlen(str) - 1;
  while(end > str && isspace((unsigned char)*end)) end--;
  // Write new null terminator character
  end[1] = '\0';
  return str;
}

int check_caret(){
  int caretint;
  char * fpname;
  fpname = malloc(sizeof(char)*20);
  strcpy(fpname,"/tmp/kinto/caret");
  if( access( fpname, F_OK ) != -1 ) {
    char *buffer = NULL;
    size_t size = 0;
    FILE *fp = fopen(fpname, "r");
    if (fp == NULL){
        return (0);
    }
    fseek(fp, 0, SEEK_END);
    size = ftell(fp);
    rewind(fp);
    buffer = malloc((size + 1) * sizeof(*buffer));
    fread(buffer, size, 1, fp);
    buffer[size] = '\0';
    trimwhitespace(buffer);
    caretint = atoi(buffer);
    fclose(fp);
    if(caretint == 1){
      // printf("caret: %s\n", buffer);
      return 1;
    }
    // printf("found nothing\n");
    return 0;
  }
  else{
    // printf("file %s does not exist\n",fpname);
    return 0;
  }
}

void *inputToggle(void *argStruct) {
  ThreadArgs args = argStruct;

  char * onInput;
  char * offInput;
  onInput = malloc(sizeof(char)*400);
  offInput = malloc(sizeof(char)*400);
  onInput = args->run_onInput;
  offInput = args->run_offInput;

  Bool ran_onInput = 0;

  while(input_check){
    if(check_caret() && ran_onInput == 0){
      if(debug == true){
        printf("run_onInput: %s\n",onInput);
      }
      system(onInput);
      ran_onInput = 1;
    }
    else if(!check_caret() && ran_onInput == 1){
      if(debug == true){
        printf("run_offInput: %s\n",offInput);
      }
      system(offInput);
      ran_onInput = 0;
    }
    sleep_ms(100);
  }
  pthread_exit(NULL);
}

void *nextPlease(void *threadid) {
  long tid;
  tid = (long)threadid;

  // printf("Next Please Thread ID, %ld\n", tid);

  // Reference http://www.rahul.net/kenton/xproto/xevents_errors.html
  // event type 17 - DestroyNotify
  // event type 18 - UnmapNotify
  // event type 22 - ConfigureNotify
  // Dismiss the following events by initiating another XNextEvent
  XNextEvent(d, &e);
  while(e.type != ConfigureNotify || (e.type == ConfigureNotify && last_event == ConfigureNotify && timeInMilliseconds()-event_ts < 419)){
    XNextEvent(d, &e);
  }
  // Unset input thread
  input_check = 0;
  last_event = e.type;

  if(debug == true){
    printf("  event: %s %d\n",eventNames[e.type-1],e.type);
    printf("  duration: %lldms\n",timeInMilliseconds()-event_ts);
  }
  event_ts = timeInMilliseconds();
  
  pthread_exit(NULL);
}

char * append(char * string1, char * string2){
  char * result = NULL;
  asprintf(&result, "%s,%s", string1, string2);
  return result;
}

static int wait_fd(int fd, double seconds){
  struct timeval tv;
  fd_set in_fds;
  FD_ZERO(&in_fds);
  FD_SET(fd, &in_fds);
  tv.tv_sec = trunc(seconds);
  tv.tv_usec = (seconds - trunc(seconds))*1000000;
  return select(fd+1, &in_fds, 0, 0, &tv);
}

Bool xerror = False;

int in_int(int a[],int size,int item){ 
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

int strcicmp(char const *a, char const *b){
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

Window get_focus_window(Display* d, int etype, char const *eventName, char const *current_app, bool debug){
  Window w;
  int revert_to;

  if(debug == true){
    printf("\n  get focus window\n");
  }

  if(!(etype == DestroyNotify || etype == UnmapNotify)) {
    XGetInputFocus(d, &w, &revert_to); // see man
    if(debug == true){
      printf("  -%s: event: %d, window_id: %ld\n",current_app,etype,w);
    }
  }

  if(xerror){
    printf("*Error getting focused window, e.type: %d, current_app: %s\n",etype,current_app);
    exit(1);
  }else if(w == None){
    printf("*no focus window, e.type: %d, current_app: %s\n",etype,current_app);
    exit(1);
  }

  return w;
}

// get the top window.
// a top window have the following specifications.
//  * the start window is contained the descendent windows.
//  * the parent window is the root window.
Window get_top_window(Display* d, Window start, int etype, char const *eventName, char const *current_app, bool debug){
  Window w = start;
  Window parent = start;
  Window root = None;
  Window *children;
  unsigned int nchildren;
  Status s;
  char * ws;
  char * wstr;
  ws = malloc(sizeof(char)*4096);
  wstr = malloc(sizeof(char)*100);
  // strcpy(wstr,"test,");

  if(debug == true){
    printf("\n  get top window\n");
  }
  // Checking for Destroy and Unmap Notify events here too
  // Sometimes they still get passed through and if so need
  // to be ignored or XQueryTree will cause a segmentation fault
  while (parent != root && parent != 0 && !(etype == DestroyNotify || etype == UnmapNotify)) {
    w = parent;

    s = XQueryTree(d, w, &root, &parent, &children, &nchildren); // see man
    
    sprintf(wstr, "%ld", w);
    if ((ws != NULL) && (ws[0] == '\0')) {
      strcpy(ws,wstr);
    }
    else{
      ws = append(ws, wstr);
    }

    if (s)
      XFree(children);

    if(xerror){
      printf("*fail to get top window: %ld, e.type: %d, current_app: %s\n",w,etype,current_app);
      break;
    }
  }

  if(debug == true){
    printf("  -%s: event: %d, window_id: %s\n",current_app,etype,ws);
  }

  return w;
}

// search a named window (that has a WM_STATE prop)
// on the descendent windows of the argment Window.
Window get_named_window(Display* d, Window start, int etype, char const *eventName, char const *current_app, bool debug){
  Window w;

  if(debug == true){
    printf("\n  get named window\n");
  }
  // printf("getting named window ... ");
  w = XmuClientWindow(d, start); // see man

  if(debug == true){
    printf("  -%s: event: %d, window_id: %ld\n\n",current_app,etype,w);
  }
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

int main(int argc, char *argv[]){

  XInitThreads();

  if(argc < 2){
    debug = false;
  }
  if(argc > 1 && (strcmp(argv[1], "-d") == 0 || strcmp(argv[1], "--debug") == 0 )){
    debug = true; 
    printf("Running in debug mode\n");  
  }

  FILE *fp;
  char buffer[10240];
  struct json_object *parsed_json, *config, *config_obj, 
  *config_obj_name, *config_obj_run, *config_obj_run_oninput, 
  *config_obj_run_offinput, *config_obj_de, *config_obj_appnames,
  *appnames_obj, *init, *de, *de_obj, *de_obj_id, *de_obj_active, 
  *de_obj_run, *de_obj_runterm,*de_obj_rungui;

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
  const char *run_oninput_array[arraylen];
  const char *run_offinput_array[arraylen];
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
    config_obj_run_oninput = json_object_object_get(config_obj, "run_onInput");
    config_obj_run_offinput = json_object_object_get(config_obj, "run_offInput");

    name_array[i] = json_object_get_string(config_obj_name);
    run_array[i] = json_object_get_string(config_obj_run);
    run_oninput_array[i] = json_object_get_string(config_obj_run_oninput);
    run_offinput_array[i] = json_object_get_string(config_obj_run_offinput);
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

  char *name;

  // for XmbTextPropertyToTextList
  setlocale(LC_ALL, ""); // see man locale

  d = open_display();
  XSelectInput(d, DefaultRootWindow(d), SubstructureNotifyMask);
  XSetErrorHandler(handle_error);

  char * run_normal;
  char * run_onInput;
  char * run_offInput;
  char * prior_app;
  char * current_app;
  char * prior_category;
  char * current_category;
  run_onInput = malloc(sizeof(char)*400);
  run_offInput = malloc(sizeof(char)*400);
  run_normal = malloc(sizeof(char)*400);
  prior_app = malloc(sizeof(char)*100);
  current_app = malloc(sizeof(char)*100);
  prior_category = malloc(sizeof(char)*100);
  current_category = malloc(sizeof(char)*100);
  strcpy(prior_app,"none");
  strcpy(prior_category,"none");

  int remap_bool = 2;

  printf("Starting keyswap...\n");

  // get active window
  w = get_focus_window(d, 0, eventNames[0], current_app, debug);
  w = get_top_window(d, w, 0, eventNames[0], current_app, debug);
  w = get_named_window(d, w, 0, eventNames[0], current_app, debug);

  // XFetchName(d, w, &name);
  // printf("window:%#x name:%s\n", w, name);
  printf("First window name: %s \n\n",str_window_class(d, w,prior_app));

  int breakouter;
  last_event=0;
  event_ts = timeInMilliseconds();

  for (;;)
  {
    strcpy(current_app,str_window_class(d, w,prior_app));
    int category_idx;
    // printf("current: %s\n",current_app);
    breakouter = 0;

    // Cycle through category name array
    // printf("%d\n",arraylen);
    for(i = 0; i < arraylen; ++i){
      // Cycle through the maximum App name array in each category
      for(n = 0; n < appnames_max; ++n){
        if (appnames_array[i][n] != NULL){
          // printf("%s\n",appnames_array[i][n]);
          if(strcicmp(appnames_array[i][n], current_app) == 0){
            strcpy(current_category,name_array[i]);
            category_idx = i;
            // printf("Match found: %s: %s\n",current_category,current_app);
            breakouter = 1;
            break;
          }
        }
        else if(i == arraylen-1 && breakouter==0){
          // printf("No match found, default to gui");
          strcpy(current_category,"gui");
          category_idx = in(name_array, arraylen, current_category);
          // printf("Match found: %s: %s\n",current_category,current_app);
          break;
        }
        else if(appnames_array[i][n] == NULL){
          break;
        }
        if(breakouter==1){
          break;
        }
      }
    }
    if(strcicmp(prior_category, current_category) != 0){
      // printf("prior: %s, current: %s\n",prior_category,current_category);
      // printf("%d,%d,%d,%d\n",strcicmp(prior_category, "gui"),strcicmp(current_category, "firefox"),strcicmp(current_category, "gui"),strcicmp(prior_category, "firefox"));
      // printf("%d,%d\n",(strcicmp(prior_category, "gui") != 0 && strcicmp(prior_category, "firefox") != 0),(strcicmp(current_category, "gui") != 0 && strcicmp(current_category, "firefox") != 0));
      printf("%s: %s\n",current_category,current_app);
      // Make sure we're not switching between 2 GUI keymaps
      // Firefox & Standard GUI apps
      // strcicmp returns 0 for matches, <>0 for non-match
      if((strcicmp(prior_category, "gui") != 0 && strcicmp(prior_category, "firefox") != 0) || (strcicmp(current_category, "gui") != 0 && strcicmp(current_category, "firefox") != 0)){
        if(debug == true){
          printf("run: %s\n",run_array[category_idx]);
        }
        system(run_array[category_idx]);
      }
      strcpy(run_normal,run_array[category_idx]);
      strcpy(run_onInput,run_oninput_array[category_idx]);
      strcpy(run_offInput,run_offinput_array[category_idx]);
      system(run_offInput);
      for(r = 0; r < config_de_max; r++){
        if(config_de_array[category_idx][r] != -1){
          int de_id_idx = in_int(de_id_array, de_len, config_de_array[category_idx][r]);
          if(strcicmp(current_category, "term") == 0){
            if(debug == true){
              printf("Running de term command: %s\n",de_runterm_array[de_id_idx]);
            }
            system(de_runterm_array[de_id_idx]);
          }
          else{
            if(debug == true){
              printf("Running de gui command: %s\n",de_rungui_array[de_id_idx]);
            }
            system(de_rungui_array[de_id_idx]);
          }
        }
      }
    }
    else if(strcicmp(prior_app, current_app) != 0){
      int indent = strlen(current_category)+2;
      printf("%*c%s\n", indent, ' ',current_app);
    }

    fflush(stdout);

    strcpy(prior_app,current_app);
    strcpy(prior_category,current_category);

    if(strlen(run_onInput) > 0){
      input_check = 1;
    }
    else{
      input_check = 0;
    }

    pthread_t threads[NUM_THREADS];
    int rc;
    int i;
    ThreadArgs args = (ThreadArgs)malloc(sizeof(struct threadArgs));
    args->run_onInput = run_onInput;
    args->run_offInput = run_offInput;
    for( i = 0; i < NUM_THREADS; i++ ) {

      if(i==0){
        rc = pthread_create(&threads[i], NULL, inputToggle, args);
      }
      else{
        rc = pthread_create(&threads[i], NULL, nextPlease, (void *)&i);
      }
      if (rc) {
        printf("Error:unable to create thread, %d\n", rc);
        exit(-1);
      }
    }
    // wait for threads to close before continuing
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);  
    }

    w = get_focus_window(d, e.type, eventNames[e.type-1], current_app, debug);
    w = get_top_window(d, w, e.type, eventNames[e.type-1], current_app, debug);
    w = get_named_window(d, w, e.type, eventNames[e.type-1], current_app, debug);
  }
}