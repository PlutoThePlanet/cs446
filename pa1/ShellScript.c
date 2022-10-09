// ShellScript.c
// Amber Hankins, Paige Mortensen
// CS446 PA 1 - Creating a shell

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <unistd.h> 
#include <fcntl.h>
#include <errno.h>
#include <sys/stat.h>
#include <stdbool.h>

//function prototypes
void promptUser(bool isBatch);
void printError();
int parseInput(char *input, char *splitWords[]);
char* redirectCommand(char *special, char *line, bool *isRedirect, char *tokens[], char *outputTokens[]);
char* executeCommand(char *cmd, bool *isRedirect, char* tokens[], char* outputTokens[],  bool *isExits);
void printHelp(char *tokens[], int numTokens);
bool exitProgram(char *tokens[], int numTokens);
void launchProcesses(char *tokens[], int numTokens, bool isRedirect);
void changeDirectories(char *tokens[], int numTokens);

//main
int main(int argc, char *argv[]){ 
    FILE *input = NULL;
    FILE *output = NULL;
    FILE *redirect = NULL;
    char curLine[100];
    char *words = NULL;
    bool batch = false;
    bool redirecting = false;
    int args = 0;
    bool isExits = false;
    char *cmd;
    bool isRedirect = false;
    char *tokens[100] = {'\0'};
    char *outputTokens[100] = {'\0'};

    // testing for batch
    if(argc == 1){
        batch = false;
        input = stdin;
    } else if(argc == 2 && strcmp(argv[1], "batchf") == 0){
        batch = true;
        input = fopen("batch.txt","r");

        // running batch commands
        fgets(curLine, 100, input);
        words = strtok(curLine, " \n");
        while( words != NULL ) {
            tokens[args] = words;
            words = strtok(NULL, " \n");
            args++;
        } 
        printf("%s\n", curLine);
        executeCommand(tokens[0], &isRedirect, tokens, outputTokens, &isExits);
        // clear used variables
        words = NULL;
        args = 0;
        // char *tokens[100] = {'\0'}; // may have to iterate through everything again
    } else if(argc == 2 && strcmp(argv[1], "batchf") != 0){
        printf("Invalid argument, please enter ./PA1 or ./PA1 batchf\n");
        isExits = true;
    } else if(argc > 2){
        printf("Too many arguments, please enter ./PA1 or ./PA1 batchf\n");
        isExits = true;
    }

    // user input & usage
    while(!isExits){ 
        args = 0;
        promptUser(batch);
        fgets(curLine, 100, input);
        words = strtok(curLine, " \n");

        while( words != NULL ) {
            tokens[args] = words;
            words = strtok(NULL, " \n");
            args++;
        } 

        executeCommand(tokens[0], &isRedirect, tokens, outputTokens, &isExits);
        
            //printHelp(tokens, args);
            //changeDirectories(tokens, args);    
            //exiting = exitProgram(tokens, args);
    }

    fclose(input);
}

//function definitions
void promptUser(bool isBatch){
    if(!isBatch){
        char* username = getenv("USER");
        char hostname[1024];
        gethostname(hostname, 1024);
        char cwd[1024];
        char* directory = getcwd(cwd, sizeof(cwd));
        printf("%s@%s:%s$ ", username, hostname, directory);
    }
}

void printError(){
    printf("Shell Program Error Encountered\n");
}

int parseInput(char *input, char *splitWords[]){
    int wordInd = 0;
    splitWords[0] = strtok(input, " ");
    while(splitWords[wordInd] != NULL){
        splitWords[++wordInd] = strtok(NULL, " ");
    }
    return wordInd;
}

char* redirectCommand(char *special, char *line, bool *isRedirect, char *tokens[], char *outputTokens[]){
    FILE *in = NULL;
    FILE *out = NULL;
    char *content[100];
    *isRedirect = true;
    *outputTokens = strtok(*tokens, " ");
    char *middle = outputTokens[1];
    char *end = outputTokens[3];
    char *outputfilename = outputTokens[2];
    if(!(in = fopen(outputTokens[0], "r")) || !(out = fopen(outputTokens[2], "w")) || (middle != ">") || (end != NULL)){
        printError();
        *isRedirect = false;
        return outputfilename;
    } else {
        fread(content, sizeof(content), 1, in);
        fwrite(content, sizeof(content), 1, out);
        return outputfilename;
    }
}

char* executeCommand(char *cmd, bool *isRedirect, char *tokens[], char *outputTokens[],  bool *isExits){ // driver fct for launchProcesses
    char *copyCMD = strdup(cmd);        // Use strdup() to make a copy of the command
    strcat(copyCMD, "\n");              // Use strcat to append a new line character ("\n") to the command, so that the system recognizes it
    char *outputFile = "";              // Create another char* for the output file name, and initialize it to an empty string
    *isRedirect = strchr(cmd, '>');     // Use strchr to check if a redirect symbol ('>') is used, and store the return in an appropriate variable.
    char *filename;
    int numTokens = 0;
    int i = 0;
    
    while(tokens[i] != NULL){
        i++;
    }
    
    if(*isRedirect == true){                                                               // If the return from strchr is not null, 
        char *filename = redirectCommand(NULL, NULL, isRedirect, tokens, outputTokens);    // then you should call redirectCommand (which returns the output file name, so store it), 
        return filename;                                                                   // and return the output file name from this function. 
    } else if(*isRedirect == false){                                                        // If the return from strchr is null, 
        numTokens = parseInput(cmd, outputTokens);                                         // then you should parseInput (storing the number of returned tokens). 
        if(numTokens == 0){                                                                // If the number of returned tokens is 0,  
            return filename;                                                               //return from the function.
        }else if(numTokens == 0){                                                          // if the return is null, 
            exitProgram(tokens, i);                                                        // call exitProgram
            *isExits = true;                                                               // and set the exit bool parameter so that main will know to exit the program
        }
    }

    if(*isRedirect == true){                                                           // If the user has chosen to exit,
        return filename;                                                               // you should immediately return the output file name. 
    } else{     
        *isExits = exitProgram(tokens, i);                                                                        // Otherwise, you should call
        changeDirectories(tokens, i);
        printHelp(tokens, i);
        launchProcesses(tokens, i, &isRedirect); //SEG FAULTING
        return filename;
    }
    free(copyCMD);
    return cmd;
}

void printHelp(char *tokens[], int numTokens){
    if(strcmp(tokens[0], "help") == 0 && numTokens == 1){
        printf("\nExample linux shell.\nThese shell commands are defined internally.\nhelp -prints this screen so you can see the available shell commands.\ncd -changes directories to specified path; if not given, defaults to home.\nexit -closes the example shell.\n[input] > [output] -pipes input file into output file.\n\n");
    } else if(strcmp(tokens[0], "help") == 0 && numTokens != 1){
        printError();
    }
}

bool exitProgram(char *tokens[], int numTokens){
    if(strcmp(tokens[0], "exit") == 0 && numTokens == 1){
        return true;
    } else if(strcmp(tokens[0], "exit") == 0 && numTokens != 1){
        printError();
        return false;
    } else {
        return false;
    }
}

void launchProcesses(char *tokens[], int numTokens, bool isRedirect){
    // print();
    for(int i=0; i<100; i++){
        if(tokens[i] != NULL){                                               // while there are still tokens to pull from
           /*
            if(fork() != 0){                                        // create a child process ID, check it's not 0 // fork() returns process ID # // 0 is parent process
                int error = -5;                                      // The return from execvp should be stored to check for errors
                error = execvp(tokens[0], tokens);                  // get command (first token) // call execvp(command, tokens) // passed
                if(error != -5){ 
                    //if((tokens[0] != 'exit') || (tokens[0] != 'help') || (tokens[0] != 'cd')){
                    // }else{ // C is a short-circuit language, so this is needed
                        printError();
                    // }
                }
                int status = 0; // wait for child process to finish before parent runs
                if (wait(&status) == -1){ // wait(): on success, returns the process ID of the terminated child; on failure, -1 is returned     // while(*status != NULL){} // loop until pid_t is returned
                    printError();
                } 
            }
            */
        }
    }
}

void changeDirectories(char *tokens[], int numTokens){
    if(strcmp(tokens[0], "cd") == 0 && numTokens == 2){
        chdir(tokens[1]);
    } else if(strcmp(tokens[0], "cd") == 0 && numTokens != 2){
        printError();
    }
}