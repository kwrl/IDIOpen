import java.lang.*;
public class Loop_threads extends Thread{
	String printNumber;
	
	Loop_threads(String printNumber) {
		this.printNumber = printNumber;
	}

	public void run() {
		System.out.println(printNumber);
		try
		{
			Thread.sleep(50000000);
		}
		catch (InterruptedException e) 
		{
			System.out.println("exception" + e);
		}	
	}


	public static void main (String [] args) {
		int i = 0;
		while (true) {
			try
			{
				new Loop_threads("20").start();
			}
			catch(OutOfMemoryError E) 
			{	
				continue;	
			}
			i++;
			System.out.println("ny thread" + i);		
		}
	}
} 
