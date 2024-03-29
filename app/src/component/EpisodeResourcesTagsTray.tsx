import * as React from 'react';
import { Box, Chip } from '@mui/material';
import { stringToColor } from './colorCache';
import { Tag } from '../proto/base/tag';


export interface EpisodeResourcesTagsTrayParam {
    tags: Tag[] | string[];
    selectedTags?: Set<string>;
    onClick?: (tag: Tag) => void;
    size?: 'small' | 'medium';
}

export function EpisodeResourcesTagsTray(param: EpisodeResourcesTagsTrayParam) {
    const { tags, selectedTags, onClick, size } = param;
    if (!tags) {
        return <></>;
    }

    let elems = tags.map((tag, index) => {
        tag = convert(tag);
        const onTagClicked = onClick ? () => { onClick(tag); } : undefined;

        const selected = (selectedTags && selectedTags.has(tag.tag));


        const variant = selected ? "filled" : "outlined";
        const onDelete = selected ? undefined : undefined;


        const colorCode = selected ? stringToColor(tag.tag, 0.2) : stringToColor(tag.tag, 0.9);
        let theme = selected ? {
            backgroundColor: colorCode
        } : {
            color: colorCode,
            borderTopColor: colorCode,
            borderRightColor: colorCode,
            borderLeftColor: colorCode,
            borderBottomColor: colorCode
        };

        return <Chip key={index} sx={theme} size={size ? size : "small"} label={tag.tag} className="mx-1" variant={variant} onClick={onTagClicked} onDelete={onDelete} clickable={false} />;
    });

    return <Box>
        {elems}
    </Box>;
}



function isString(value: any): value is String {
    return typeof value === 'string';
}

export function convert(t: Tag | String): Tag {
    if (isString(t)) {
        return new Tag({ tag: String(t) })
    } else {
        return t
    }
}
