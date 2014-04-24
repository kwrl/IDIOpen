import java.util.Arrays;
import java.lang.OutOfMemoryError;

import java.util.ArrayList;

class Error2
{
	public static void main(String[] args)
	{
        ArrayList<int[]> alList = new ArrayList<int[]>();

        for(;;)
        {
            try
            {
                alList.add(new int[1000]);
            }
            catch(OutOfMemoryError oome)
            {
                continue;
            }
        }
	}
 
    public static int[] countingSort(int[] a, int low, int high)
    {
        int[] counts = new int[high - low + 1]; // this will hold all possible values, from low to high
        for (int x : a)
            counts[x - low]++; // - low so the lowest possible value is always 0
     
        int current = 0;
        for (int i = 0; i < counts.length; i++)
        {
            Arrays.fill(a, current, current + counts[i], i + low); // fills counts[i] elements of value i + low in current
            current += counts[i]; // leap forward by counts[i] steps
        }

        return counts;
    }
}

/* EOF */
