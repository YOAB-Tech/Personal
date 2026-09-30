const ICONS = {
    folder: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>',
    file:   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>'
};
const filelist = document.getElementById("file-list");
const fileempty = document.getElementById("file-empty");
const user = filelist.dataset.user;
async function loadingpage(){
    document.querySelectorAll('.file-row').forEach(row => row.remove());
    const response = await fetch(`/api/files/${user}`);
    const data = await response.json();
    console.log(data);
    return data;
}
async function init(){
    const data = await loadingpage();
    data.forEach(function(item){
    permutation.push(item);
    const row = document.createElement('div');
    row.className = "file-row";
    const icon = document.createElement('span');
    icon.className = 'file-icon';
    if(item.is_dir){
        icon.innerHTML = ICONS.folder;
    }
    else{icon.innerHTML = ICONS.file;}
    row.append(icon);
    const name = document.createElement('span');
    name.className = "file-name";
    name.innerHTML = `${item.filename}`;
    const size = document.createElement('span');
    size.className = "file-size";
    itemsize = formatsize(item.filesize);
    size.innerHTML = `${itemsize}`;
    const modified = document.createElement('span');
    modified.className = "file-modified";
    modified.innerHTML = timeAgo(item.date);
    row.append(name);
    row.append(size);
    row.append(modified);
    filelist.appendChild(row);
});
}
init();
permutation = [];
function mergesort(inputlist){
    if(inputlist.length === 1){
        return inputlist;
    }
    const mid = Math.floor(inputlist.length/2);
    const right = inputlist.slice(mid);
    const left = inputlist.slice(0,mid)
    mergesort(right)
    mergesort(left)
    let i = 0
    let j = 0
    let k = 0
    while(i < right.length && j < left.length){
        if(right[i]<=left[j]){
            inputlist[k] = right[i];
            i ++;
            k++;
        }
        else{
            inputlist[k] = left[j];
            j++;
            k++;
        }
    }
    while(i<right.length){
        inputlist[k] = right[i];
        i++;
        k++
    }
    while(j<left.length){
        inputlist[k] = left[j];
        j++;
        k++;
    }
}
function timeAgo(isoString) {
    const then = new Date(isoString);
    const diffMs = Date.now() - then.getTime();
    const seconds = Math.floor(diffMs / 1000);

    if (seconds < 60) return "just now";
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return minutes + "m ago";
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return hours + "h ago";
    const days = Math.floor(hours / 24);
    if (days < 30) return days + "d ago";
    const months = Math.floor(days / 30);
    if (months < 12) return months + "mo ago";
    return Math.floor(months / 12) + "y ago";
}
function formatsize(byte){
    if (byte<1024){return byte.toString() + ' B';}
    if(byte < 1024 * 1024) {return (byte/1024).toFixed(1).toString() + ' KB';}
    else{return (byte /1024 / 1024).toFixed(1).toString() + ' MB';}
}
