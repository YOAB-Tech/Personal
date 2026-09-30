public class intlist{
    public int first;
    public intlist next;
    public intlist(int f, intlist l){
        first = f;
        next = l;
    }
    public int size(){
        if(this.next == null){
            return 1;
        }
        return 1+this.next.size();
    }
    public int get(int i){
        if(i == 1){
            return this.first;
        }
        else{
            return this.next.get(i-1);
        }
    }
    public static void main(String[] args) {
        intlist L = new intlist(100,null);
        L = new intlist(15, L);
        L = new intlist(89, L);
        System.out.println(L.size());
        System.out.println(L.get(3));
    }
}