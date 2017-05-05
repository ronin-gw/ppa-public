#include <stdio.h>
#include <stdlib.h>

void printError ( void )
{
  printf ( "ERROR\n" );
  exit ( EXIT_FAILURE );
}

void show ( int *array, int num )
{
  int i;
  for ( i = 0; i < num-1; i++ )
    {
      printf ( "%d ", array[ i ] );
    }
  printf ( "%d\n", array[ num-1 ] );
}

int merge ( int *array, int p, int q, int r )
{ 
  int count = 0;
  int n_1 = q - p + 1, n_2 = r - q;
  int *leftArray, *rightArray;
  int i, tmp1, tmp2, index;

  if ( ( leftArray = ( int * ) malloc ( n_1 * sizeof ( int ) ) ) == NULL )
    {
      printError();
    }
  for ( i = 0; i < n_1; i++ )
    {
      leftArray[ i ] = array[ p + i ];
    }

  if ( ( rightArray = ( int * ) malloc ( n_2 * sizeof ( int ) ) ) == NULL )
    {
      printError();
    }
  for ( i = 0; i < n_2; i++ )
    {
      rightArray[ i ] = array[ q + i + 1 ];
    }

  index = p;
  tmp1 = 0;
  tmp2 = 0;
  while ( ( tmp1 < n_1 ) && ( tmp2 < n_2 ) )
    {
      if ( leftArray[ tmp1 ] <= rightArray[ tmp2 ] )
	{
	  array[ index ] = leftArray[ tmp1 ];
	  tmp1++;
	}
      else
	{
	  array[ index ] = rightArray[ tmp2 ];
	  tmp2++;
	}

      index++;
      count++;
    }


  if ( tmp1 < n_1 )
    {
      while ( tmp1 < n_1 )
	{
	  array[ index ] = leftArray[ tmp1 ];
	  tmp1++;
	  index++;
	}
    }
  else
    {
      while ( tmp2 < n_2 )
	{
	  array[ index ] = rightArray[ tmp2 ];
	  tmp2++;
	  index++;
	}
    }

  free ( leftArray );
  free ( rightArray );
  
  return count;
}

int main ( int argc, char *argv[] )
{
  int num, tmp, count;
  int p, q, r;
  int *data;
  
  // �ǡ����θĿ����ɤ߹���
  if ( scanf ( "%d", &num ) == EOF )
    {
      printError();
    }

  // �ޡ����ϰϤ��ɤ߹���
  if ( scanf ( "%d %d %d", &p, &q, &r ) == EOF )
    {
      printError();
    }

  // �ǡ������ɤ߹���
  if ( ( data = ( int * ) malloc ( num * sizeof ( int ) ) ) == NULL )
    {
      printError();
    }
  tmp = 0;
  while ( ( scanf ( "%d", data + tmp ) != EOF ) || tmp < num )
    {
      tmp++;
    }

  // �ޡ�����Ԥʤ�
  count = merge ( data, p, q, r );

  // ɽ������
  show ( data, num );
  printf ( "%d\n", count );

  free ( data );

  return 0;
}