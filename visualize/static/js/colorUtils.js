const findLayer=  (data) => {
    if (!("children" in data)) {
        return 1
    }
    let layer = 0;
    data = data["children"]
    for (let i in data) {
        let datum = data[i]
        layer = Math.max(layer, findLayer(datum))
    }
    return layer + 1;
}

const attachColorItem = (data, colors, layer) => {
    if (!("children" in data)) {
        return !data.circle || (data.color = colors[layer])
    }
    data.color = colors[layer]
    data = data["children"]
    for (let i in data) {
        let datum = data[i]
        attachColorItem(datum, colors, layer + 1)
    }
}

const attachColor = (data, color) => {
    attachColorItem(data, generateGradientColors(color, findLayer(data)), 0)
}
function colorNameToHex(colorName) {
    const colors = {
        "red": "#FF0000",
        "green": "#008000",
        "blue": "#0000FF",
        "yellow": "#FFFF00",
        "orange": "#FFA500",
        "purple": "#800080",
        "pink": "#FFC0CB",
        "cyan": "#00FFFF",
        "magenta": "#FF00FF",
        "lime": "#00FF00",
        "gray": "#808080",
        "navy": "#000080",
        "teal": "#008080",
        "aqua": "#00FFFF",
        "olive": "#808000",
        "maroon": "#800000",
        "brown": "#A52A2A",
        "black": "#000000",
        "white": "#FFFFFF",

    };
    return colors[colorName.toLowerCase()] || colorName;
}

function lightenHexColor(hex, amount) {
    let r = parseInt(hex.substring(1, 3), 16);
    let g = parseInt(hex.substring(3, 5), 16);
    let b = parseInt(hex.substring(5, 7), 16);

    // 确保增加的亮度不会超过255
    r = Math.min(255, r + Math.round(amount));
    g = Math.min(255, g + Math.round(amount));
    b = Math.min(255, b + Math.round(amount));

    // 将更新后的 RGB 值转换回十六进制格式，并确保长度为2
    r = r.toString(16).padStart(2, '0');
    g = g.toString(16).padStart(2, '0');
    b = b.toString(16).padStart(2, '0');

    return `#${r}${g}${b}`;
}

function generateGradientColors(colorName, levels) {
    const hexColor = colorNameToHex(colorName);
    if (!hexColor) {
        console.error("Unsupported color name.");
        return;
    }

    const gradientColors = [];
    const amountToLighten = Math.round((255 / levels) / 1.5);  // 根据层级计算增亮的幅度，并四舍五入到最近的整数

    for (let i = 0; i < levels; i++) {
        const lighterColor = lightenHexColor(hexColor, amountToLighten * i);
        gradientColors.push(lighterColor);
    }
    gradientColors.reverse()
    return gradientColors;
}
export {
    attachColor
}