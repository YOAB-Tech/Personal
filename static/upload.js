const fileinput = document.getElementById('file-input');
const folderinput = document.getElementById('folder-input');
const count = document.getElementById('preview-count');
const sizesum = document.getElementById('preview-size');
const previewlist = document.getElementById('preview-list');
const folder = folderinput.files;
sizesum.innerHTML = `0 MB`;
count.innerHTML = `0 files`;
var size = 0;
var number = 0;
previewlist.querySelectorAll('.preview-row').forEach(row => row.remove());
folderinput.addEventListener("change",function(){
    document.getElementById('preview-empty').style.display = 'none';
    let localsize = 0;
    const files = Array.from(folderinput.files)
    for(const file of files){
        size += file.size
        localsize += file.size
        number+= 1;
    }
    totalsize = formatsize(size);
    localsize = formatsize(localsize);
    const foldername = files[0].webkitRelativePath.split('/')[0];
    sizesum.innerHTML = `${totalsize}`;
    count.innerHTML = `${number} files`;
    const row = document.createElement('div');
    row.className = 'preview-row';
    const icon = document.createElement('span');
    icon.className = 'preview-icon'
    icon.innerHTML = '📂';
    const name = document.createElement('span');
    name.className = 'preview-name';
    name.innerHTML = `${foldername}`;
    const foldersize = document.createElement('span');
    foldersize.className = 'preview-size';
    foldersize.innerHTML = `${localsize}`;
    row.append(icon);
    row.append(name);
    row.append(foldersize);
    previewlist.appendChild(row)
});
fileinput.addEventListener("change", function(){
    document.getElementById('preview-empty').style.display = 'none';
    let files = fileinput.files;
    for(const file of files){
        size += file.size
        number+= 1;
        totalsize = formatsize(size);
        sizesum.innerHTML = `${totalsize}`;
        count.innerHTML = `${number} files`;
        const row = document.createElement('div');
        row.className = 'preview-row';
        const icon = document.createElement('span');
        icon.className = 'preview-icon'
        icon.innerHTML = '📄';
        const name = document.createElement('span');
        name.className = 'preview-name';
        name.innerHTML = `${file.name}`;
        const foldersize = document.createElement('span');
        foldersize.className = 'preview-size';
        foldersize.innerHTML = `${formatsize(file.size)}`;
        row.append(icon);
        row.append(name);
        row.append(foldersize);
        previewlist.appendChild(row)
    }
});

function formatsize(byte){
    if (byte<1024){return byte.toString() + ' B';}
    if(byte < 1024 * 1024) {return (byte/1024).toFixed(1).toString() + ' KB';}
    else{return (byte /1024 / 1024).toFixed(1).toString() + ' MB';}
}



