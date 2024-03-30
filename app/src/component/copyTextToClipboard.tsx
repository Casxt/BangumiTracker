



export async function copyTextToClipboard(text: string): Promise<boolean> {
    try {
        await navigator.clipboard.writeText(text);
        // console.log('Text copied to clipboard');
        return true;
    } catch (err) {
        console.error('Failed to copy text: ', err);
        return false;
    }
}
