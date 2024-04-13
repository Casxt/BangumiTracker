
import { Box, Container, Link, Typography } from "@mui/material";
import React, { useEffect, useState } from "react";

import { getBangumiIndex } from "../api/api";

import { BangumiIndex } from "../proto/bangumi/bangumi";
import { Bangumi } from "../proto/bangumi/bangumi";


export function FullBangumiPage() {
    const [bangumiIndex, setBangumiIndex] = useState(new BangumiIndex);
    useEffect(() => {
        getBangumiIndex().then(
            resp => {
                setBangumiIndex(resp.data);
            }
        )
    }, [])

    return (
        <Container maxWidth="lg" sx={{ color: 'rgb(138, 54, 49)' }}>
            <Box my={2}>
                {bangumiIndex.index.map((anime: Bangumi) => (
                    <Link key={anime.id} href={"/bangumi/" + anime.id} color="inherit" underline="none">
                        <Typography variant="h5" className="py-2 px-4 my-1 rounded-lg hover:bg-[#FFE9E9] ease-in-out duration-75">
                            <Box display='inline'>
                                {`${anime.id}. `}
                            </Box>
                            <Box display='inline' className='underline underline-offset-4'>
                                {anime.names[0].name}
                            </Box>
                        </Typography>
                    </Link>
                ))}
            </Box>
        </Container>
    )
}