import java.util.Scanner;

public class ValidatePikk
{
    public static void main(String[] args) throws Exception
    {
        Scanner sc = new Scanner(System.in);
        for(int i = 0; i < 10; i++)
            if(!sc.next().equals("Pikk"))
                throw new Exception("No pikk");
    }
}
