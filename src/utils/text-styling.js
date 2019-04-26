export const StyleEnum = {
  BOLD: 1,
  ITALIC: 2,
  UNDER: 4,
  addStyle: (s, style) => s | style,
  removeStyle: (s, style) => s & ~style,
  hasStyle: (s, style) => Boolean(s & style),
  toggleStyle: (s, style) => s ^ style
};
export const textStyles = s => {
  let _style = {};
  _style.fontWeight = StyleEnum.hasStyle(s, StyleEnum.BOLD) ? "bold" : "normal";
  _style.textDecoration = StyleEnum.hasStyle(s, StyleEnum.UNDER)
    ? "underline"
    : "none";
  _style.fontStyle = StyleEnum.hasStyle(s, StyleEnum.ITALIC)
    ? "italic"
    : "normal";
  return _style;
};

export const colorFromInt = (n, N_COLORS = 8) => {
  let colorString = "#";
  for (let i = 0; i < Math.ceil(Math.log2(N_COLORS)); i++)
    colorString += ind & Math.pow(2, i) ? "f" : "0";
  return colorString;
};
