import java.lang.OutOfMemoryError;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;

import java.util.*;
public class memory_swap
{
    public static void main(String[] args)
    {
        List<MemoryManager> alList = new ArrayList<MemoryManager>();
        //List<int[]> alList2 = new ArrayList<int[]>();
        MemoryManager x = new MemoryManager(2147483647);
        for(;;)
        {
            x.incrementTotalMemory(10000);

        }
      
    }

 public static class MemoryManager implements Serializable
    {
        private static final long serialVersionUID = 1L;
        static volatile long    totalMemory;
        private static double   swapLimit     = 4;
        static final double    oneGig      = 1024 * 1024 * 1024;
        static synchronized void incrementTotalMemory(long ammount)
        {
            totalMemory += ammount;
            // System.out.println("Memory up  to " + (totalMemory / (1024 * 1024)));
        }
        static synchronized void decrementTotalMemory(long ammount)
        {
            totalMemory -= ammount;
            // System.out.println("Memory down to " + (totalMemory / (1024 * 1024)));
        }
        public static long getTotalMemory()
        {
            return totalMemory;
        }
        private void writeObject(ObjectOutputStream out) throws IOException
        {
            //System.out.println(Messages.getString("SFData.4")); //$NON-NLS-1$
            out.writeLong(this.ammount);
            //decrementTotalMemory(ammount);
            ammount = 0; // don't double count in finalizer
        }
        private void readObject(ObjectInputStream in) throws IOException
        {
            ammount = in.readLong();
            incrementTotalMemory(ammount);
        }
        private long ammount;
        public MemoryManager(final long memoryUsed)
        {
            incrementTotalMemory(memoryUsed);
            ammount = memoryUsed;
        }
        @Override
        protected void finalize()
        {
            //decrementTotalMemory(ammount);
        }
        public static boolean underLimit(long bias)
        {
            double used = (getTotalMemory() / oneGig);
            double toBeUsed = used + (bias / oneGig);
            boolean x = toBeUsed < swapLimit;
            if (!x)
            {
                //System.out.println(Messages.getString("SFData.6") + toBeUsed + Messages.getString("SFData.7") + swapLimit); //$NON-NLS-1$ //$NON-NLS-2$
                //System.gc(); // Request garbage collection
            }
            return x;
        }
        public static void setSwapLimit(double limit)
        {
            swapLimit = limit;
        }
    }
}
