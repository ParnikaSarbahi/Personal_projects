#include<stdio.h>
#include<stdlib.h>
#include<time.h>

int main(){
    int random,guess;
    int number_of_guesses=0;
    srand(time(NULL));
    printf("Welcome to Guessing Numbers Game");
    random=rand()%100+1; //Generating numbers between 1 to 100
    do{
        printf("Please enter your guess between 1-100:");
        scanf("%d",&guess);
        number_of_guesses++;

        if(guess<random){
            printf("Guess a larger number.\n");
        }else if(guess>random){
            printf("Guess a smaller number.\n");
        }else{
            printf("Congratulations!!You have successfully guessed the number in %d attempts\n",number_of_guesses);
        }
    }while(guess!=random);

    printf("Bye bye, Thanks for Playing\n");
    printf("Developed by Parnika\n");
}
