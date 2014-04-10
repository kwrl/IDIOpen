public class Test
{
    public static void main(String[] args)
    {
        for(String s : args)
        {
            int num = Integer.parseInt(s);
            System.out.print(num*num + " ");
        }
        System.out.println("");
    }
}
