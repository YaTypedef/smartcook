//
// Autogenerated by Thrift Compiler (0.9.1)
//
// DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
//


Recipe = function(args) {
  this.title = null;
  if (args) {
    if (args.title !== undefined) {
      this.title = args.title;
    }
  }
};
Recipe.prototype = {};
Recipe.prototype.read = function(input) {
  input.readStructBegin();
  while (true)
  {
    var ret = input.readFieldBegin();
    var fname = ret.fname;
    var ftype = ret.ftype;
    var fid = ret.fid;
    if (ftype == Thrift.Type.STOP) {
      break;
    }
    switch (fid)
    {
      case 1:
      if (ftype == Thrift.Type.STRING) {
        this.title = input.readString().value;
      } else {
        input.skip(ftype);
      }
      break;
      case 0:
        input.skip(ftype);
        break;
      default:
        input.skip(ftype);
    }
    input.readFieldEnd();
  }
  input.readStructEnd();
  return;
};

Recipe.prototype.write = function(output) {
  output.writeStructBegin('Recipe');
  if (this.title !== null && this.title !== undefined) {
    output.writeFieldBegin('title', Thrift.Type.STRING, 1);
    output.writeString(this.title);
    output.writeFieldEnd();
  }
  output.writeFieldStop();
  output.writeStructEnd();
  return;
};
