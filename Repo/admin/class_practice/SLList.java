public class SLList{
    private intlist sentinel;
    private int size;
    public SLList(int x){
        sentinel = new intlist(0,null );
        sentinel.next = new intlist(x, null);
        size = 1;
    }
    public SLList(){
        size = 0;
        sentinel = new intlist(0,null);
    }
    public void addFirst(int x){
        sentinel.next = new intlist(x,sentinel.next);
        size +=1;

    }
    public int getFirst(){
        return sentinel.next.first;
    }
    public void addLast(int x){
        intlist p = sentinel;
        
        while(p.next!= null){
            p = p.next;
        }
        p.next = new intlist(x,null);
        this.size +=1;
    }
    public int size(){
        return size;
    }
    /*private int size(intlist p){
        if(p.next == null){
            return 1;
        }
        else{
            return 1+ size(p.next);
        }
    } */
}