#include <stdio.h>
#include<conio.h>
void main()
{
    int n ,i,a1=0,a2=1,sum=0,temp;
 printf("Enter the limit ");
 scanf("%d",&n);
 printf("the series is %d %d ",a1,a2);
     for(i=0;i<=n;i++)
     {
         sum=a1+a2;
         printf("%d ",sum);
         temp=a1;
         a1=a2;
         a2=sum;

     }
     getch();
 }

