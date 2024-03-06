// serialize the dom to string. There must be a better way to do this.

() => { return new XMLSerializer().serializeToString(document); }
