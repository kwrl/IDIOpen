package oving_4;

import java.rmi.RemoteException;
import java.util.LinkedList;
import java.util.Queue;

public class Probe extends Thread {
	
	private Queue<Integer> probeList = new LinkedList<Integer>();
	private ServerImpl server;
	
	// Need to take in ID of transaction
	public Probe(ServerImpl server) {
		this.server = server;
	}
	
	public void run() {
		try {
			System.out.println(("Starting Probing"));
			server.sendProbe(probeList);
		} catch (RemoteException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		System.out.println("Probing ended");
	}
	
}
