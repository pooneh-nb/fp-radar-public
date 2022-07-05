function handler(event){
    if(event.origin == 'https://bar.org' && event.data == 'Ping')
    event.source.postMessage('Pong','https://bar.org')
}
window.addEventListener('message', handler);
// running at https://bar.org
foo_window.postMessage('Ping', 'https://foo.com')