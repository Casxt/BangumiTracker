
import { Box, Button, Container, Divider, FormControlLabel, FormGroup, Skeleton, Snackbar, Stack, Switch, Typography } from "@mui/material";
import React, { useCallback, useEffect, useMemo, useState } from "react";

import { getBangumiData } from "../api/api";

import { BangumiData, Episode } from "../proto/bangumi/bangumi";
import { Tag } from "../proto/base/tag";

import { useParams } from 'react-router-dom';
import { EpisodeResourcesTray } from "../component/EpisodeResourcesTray";
import { copyTextToClipboard } from '../component/copyTextToClipboard';
import { filterResourcesByTags } from '../component/filterResourcesByTags';
import { EpisodeResourcesTagsTray } from '../component/EpisodeResourcesTagsTray';


const loadingPlaceholder = ['1', '2', '3', '4'].map(i => <Box my={2} key={i}>
    <Typography variant="h4" className="py-2 px-2 underline underline-offset-8" sx={{ color: 'rgb(138, 54, 49)' }}>
        <Skeleton variant="circular" width={40} height={40} />
    </Typography>
    <Box my={2} mx={4}>
        <Skeleton />
        <Skeleton />
        <Skeleton />
    </Box>
</Box>)



export function BangumiDataPage() {
    const { bangumiID } = useParams();

    const [loadingBangumi, setLoadingBangumi] = useState(true);


    useEffect(() => {
        getBangumiData(Number(bangumiID)).then(resp => {

            setBangumiData(resp.data);
        }).finally(() => { setLoadingBangumi(false) });
    }, [bangumiID])

    const [bangumiData, setBangumiData] = useState(new BangumiData);
    const [episodeArray, setEpisodeArray] = useState(new Array<Episode>());
    const [selectedTags, setSelectedTags] = useState(new Set<string>());

    const [openSnackbar, setOpenSnackbar] = React.useState(false);
    const [descendingOrder, setDescendingOrder] = React.useState(true);

    const handleSnackbarClose = (event: React.SyntheticEvent | Event, reason?: string) => {
        setOpenSnackbar(false);
    };

    const handleOpen = useCallback(() => {
        let links = new Array<string>();
        episodeArray.forEach(episode => {
            episode.resources.
                filter(r => filterResourcesByTags(r, selectedTags)).forEach(r => {
                    if (r.share_dmhy_org) {
                        links.push(r.share_dmhy_org.magnet.url)
                    }
                })
        })
        let text = links.join("\n");
        copyTextToClipboard(text).then(
            (r: boolean) => {
                setOpenSnackbar(r);
            }
        )
    }, [episodeArray, selectedTags])

    useEffect(() => {
        const data = bangumiData.episodes.filter(episode => episode.index);
        if (descendingOrder) {
            data.sort().reverse()
        } else {
            data.sort()
        }
        setEpisodeArray(data)
    }, [descendingOrder, bangumiData])

    const onTagClicked = useCallback((tag: Tag) => {
        if (selectedTags.has(tag.tag)) {
            selectedTags.delete(tag.tag)
        } else {
            selectedTags.add(tag.tag)
        }
        setSelectedTags(new Set(selectedTags))
    }, [selectedTags])


    const handleOrderChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
        setDescendingOrder(event.target.checked);
    }, []);



    const episodeElems = useMemo(() => {
        return episodeArray.map((episode) => (
            <Box my={2} key={episode.index}>
                <Typography variant="h4" className="py-2 px-2 underline underline-offset-8" sx={{ color: 'rgb(138, 54, 49)' }}>
                    {episode.index}
                </Typography>
                <Box my={2} mx={4}>
                    <EpisodeResourcesTray episode={episode} selectedTags={selectedTags} onTagClick={onTagClicked} />
                </Box>
            </Box>
        ))
    }, [episodeArray, selectedTags])


    const filterElems = useMemo(() => {
        if (!selectedTags || selectedTags.size <= 0) {
            return <></>
        }
        return <Box>
            <Stack spacing={0} direction="row">
                <Typography variant="h5" sx={{ color: '#B84841' }}>
                    FILTER:
                </Typography>
                <Box mx={2}>
                    <EpisodeResourcesTagsTray tags={Array.from(selectedTags)}
                        selectedTags={selectedTags} onClick={onTagClicked} size="medium" />
                </Box>
            </Stack>
            <Divider className='my-2' />
        </Box>
    }, [selectedTags])



    return (
        <Container maxWidth="lg">
            <Box mx={2}>
                {filterElems}
                <FormGroup row>
                    <FormControlLabel
                        control={
                            <Button color='pink' size="small" variant="contained" onClick={handleOpen}>Copy magnet links</Button>
                        }
                        label=""
                    />
                    <FormControlLabel
                        control={
                            <Switch color='pink' size="medium" checked={descendingOrder} onChange={handleOrderChange} />
                        }
                        label="Desc"
                        labelPlacement="end"
                    />
                </FormGroup>

                <Snackbar
                    open={openSnackbar}
                    autoHideDuration={6000}
                    onClose={handleSnackbarClose}
                    message="all magnet links are copied to your clipboard"
                />

            </Box>
            <Box my={2}>
                {loadingBangumi ? loadingPlaceholder : episodeElems}
            </Box>
        </Container>
    )
}
