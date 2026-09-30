const ICONS = {
    folder: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>',
    file:   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>'
};

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
    icon.innerHTML = ICONS.folder;
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
        icon.innerHTML = ICONS.file;
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



