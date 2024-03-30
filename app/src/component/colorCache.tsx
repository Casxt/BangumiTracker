const colorCache = new Map<string, string>();
export function stringToColor(str: string, opacity: number = 1): string {
    if (str.length <= 5) {
        str += str + str;
    }
    if (colorCache.has(str)) {
        return (colorCache.get(str) as string) + opacity + ')';
    }
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    let color = 'rgba(';
    for (let i = 0; i < 3; i++) {
        const value = (hash >> (i * 8)) & 255;
        color += value + ', ';
    }
    colorCache.set(str, color);
    color += opacity + ')';
    return color;
}
