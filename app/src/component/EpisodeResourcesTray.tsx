import * as React from 'react';
import { Episode } from "../proto/bangumi/bangumi";
import { Tag } from "../proto/base/tag";
import { ExternalResource } from "../proto/base/resources";
import { Avatar, Box, Divider, IconButton, Link, Snackbar, Stack, ThemeProvider, Tooltip, Typography } from '@mui/material';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import { BorderColor } from '@mui/icons-material';
import { EpisodeResourcesTagsTray } from './EpisodeResourcesTagsTray';
import { filterResourcesByTags } from './filterResourcesByTags';
import { copyTextToClipboard } from './copyTextToClipboard';
import { theme } from '../theme';
interface EpisodeResourcesTrayParam {
    episode: Episode;
    onTagClick?: (tag: Tag) => void;
    selectedTags?: Set<string>;
}

export function EpisodeResourcesTray(param: EpisodeResourcesTrayParam) {
    const { episode, onTagClick, selectedTags } = param;

    const [openSnackbar, setOpenSnackbar] = React.useState(false);

    const handleSnackbarClose = (event: React.SyntheticEvent | Event, reason?: string) => {
        setOpenSnackbar(false);
    };
    const getOnClickCopyBtn = (resource: ExternalResource): (() => void) => {
        return () => {
            if (resource.share_dmhy_org) {
                copyTextToClipboard(resource.share_dmhy_org.magnet.url).then(
                    (r: boolean) => {
                        setOpenSnackbar(r);
                    }
                )
            }
        }
    }

    let elems = React.useMemo(() => {
        const filteredResources = episode.resources.filter((resource): boolean => filterResourcesByTags(resource, selectedTags));
        filteredResources.sort((a, b) => b.share_dmhy_org.publish_timestamp - a.share_dmhy_org.publish_timestamp);
        return filteredResources.map((resource, index) => {
            if (resource.share_dmhy_org) {
                const dmhy_data = resource.share_dmhy_org;
                return <Box key={index} className="my-2">
                    <Typography variant="subtitle1" display="block" gutterBottom>
                        <Link href={dmhy_data.page_link} underline="hover" color="inherit" target="_blank" rel="noopener" className={'underline-offset-4'}>
                            {dmhy_data.title}
                        </Link>
                    </Typography>
                    <Stack spacing={0} direction="row">
                        <Tooltip title="copy magnet link">
                            <IconButton size='small' color='pink' aria-label="copy magnet link" onClick={getOnClickCopyBtn(resource)}>
                                <ContentCopyIcon fontSize="small" />
                            </IconButton>
                        </Tooltip>
                        <EpisodeResourcesTagsTray tags={dmhy_data.tags} selectedTags={selectedTags} onClick={onTagClick} />
                    </Stack>
                    <Divider className='my-2' />
                </Box>;
            }
        })
    }, [episode, onTagClick, selectedTags]);
    return <Box>
        {elems}
        <Snackbar
            open={openSnackbar}
            autoHideDuration={6000}
            onClose={handleSnackbarClose}
            message="magnet link are copied to your clipboard"
        />
    </Box>;
}





