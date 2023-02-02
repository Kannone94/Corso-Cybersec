  GNU nano 6.4                                          EsD3W2.c                                                    
#include <stdio.h>

int gioco(){
        int score = 0;
        char risp1, risp2, risp3;
        char rispEs1 = 'a';
        char rispEs2 = 'a';
        char rispEs3 = 'a';
        // Prima domanda
        printf ("# Per cosa si usa il tipo int in C?                     #\n");
        printf ("# A) numeri interi                                      #\n");
        printf ("# B) caratteri                                          #\n");
        printf ("# C) booleani                                           #\n");
        scanf(" %c", &risp1);
        if(risp1==rispEs1){score++;}
        // Seconda domanda
        printf ("# Con che simbolo si indica un OR in C                  #\n");
        printf ("# A) !=                                                 #\n");
        printf ("# B) &&                                                 #\n");
        printf ("# C) ||                                                 #\n");
        scanf(" %c", &risp2);
        if(risp2==rispEs2){score++;}
        // Terza domanda  
        printf ("# Che comando si usa per scrivere un Output?            #\n");
        printf ("# A) printf                                             #\n");
        printf ("# B) scanf                                              #\n");
        printf ("# C) char                                               #\n");
        scanf(" %c", &risp3);
        if(risp3==rispEs3){score++;}
        return score;
}
int main () {
        printf ("########## Benvenuto al Gioco Delle domande! ############\n");
        printf ("#   Ti farò 3 domande, ogni risposta esatta vale 1     #\n");
        char nome[20] = {'\0'};
        printf ("# Per prima cosa inserisci il nome utente              #\n");
        scanf (" %s", &nome);
        char wantPlay = 'y'; 
        while(wantPlay=='y'||wantPlay=='Y'){
                int score = gioco();
                printf("#############    %c Il tuo punteggio è: %d      #########\n", nome, score); 
                printf ("# Se vuoi fare un altra partita scrivi y               #\n"); 
                scanf(" %c", &wantPlay);
                
        }
        printf("Grazie per aver giocato! Arrivederci.\n");
        return 0;

}
 


