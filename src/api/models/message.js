

class Message {
  
  constructor(id, threadId, senderId, content, color, fmt,created) {
    this.id = id;
    this.thread = threadId;
    this.senderId = senderId;
    this.content = content;
    this.color = color;
    this.fmt = fmt;
    this.created = created;

    //TODO: fix how this i implemented so more values are cached. Object structure content->fmt->color
    this._markupCache = {
      content: this.content,
      color: this.color,
      fmt: this.fmt,
      markup: undefined
    };
  }

  //TODO: Figure out implementation. Allow for hotswapping colors?
  static createMarkup(content, color, fmt) {}

  checkCache(arguments){    
      return Object.entries(this._markupCache).every((key,value)=>arguments[key] === value);
  }

  getMarkup(color=undefined,fmt=undefined){
    let arguments = {content:this.content}
    arguments.color = color?color:this.color;
    arguments.fmt = fmt?fmt:this.fmt;
    if (!this.checkCache(arguments)){
        
        this._markupCache = {...arguments, markup:this.createMarkup(...arguments)}
    }
    return this._markupCache.markup
  }

  get markup() {
    return this.getMarkup()
  };

}

export default Message