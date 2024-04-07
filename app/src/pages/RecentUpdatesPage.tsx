
import { Badge, Box, Chip, Container, Link, Stack, Typography } from "@mui/material";
import UpdateIcon from '@mui/icons-material/Update';
import React, { useEffect, useState } from "react";

import { getBangumiIndex, getDMHYTrackerData } from "../api/api";

import { BangumiIndex, Bangumi } from "../proto/bangumi/bangumi";
import { SHARE_DMHY_ORG_TRACKER, SHARE_DMHY_ORG_TRACKER_CONFIG } from "../proto/tracker/share_dmhy_org";

import Timeline from '@mui/lab/Timeline';
import TimelineItem from '@mui/lab/TimelineItem';
import TimelineSeparator from '@mui/lab/TimelineSeparator';
import TimelineConnector from '@mui/lab/TimelineConnector';
import TimelineContent from '@mui/lab/TimelineContent';
import TimelineDot from '@mui/lab/TimelineDot';
import TimelineOppositeContent, {
    timelineOppositeContentClasses,
} from '@mui/lab/TimelineOppositeContent';
function getWeekDay(date: Date): number {
    const day = date.getDay();
    if (day === 0) {
        return 7;
    }
    return day;
}

function getDaysBetween(date1: Date, date2: Date): number {
    // 将两个日期都设置为当天的凌晨 00:00:00
    const d1 = new Date(date1.getFullYear(), date1.getMonth(), date1.getDate());
    const d2 = new Date(date2.getFullYear(), date2.getMonth(), date2.getDate());
    const timeDiff = Math.abs(d1.getTime() - d2.getTime());
    return Math.ceil(timeDiff / (1000 * 3600 * 24));
}

function getDateString(isotime: string): string {
    if (!isotime) {
        return ""
    }
    const date = new Date(isotime);
    const today = new Date();
    const today_week_day = getWeekDay(today);
    const date_week_day = getWeekDay(date);
    const days_between = getDaysBetween(today, date);
    if (days_between === 0) {
        return "Today " + date.toLocaleTimeString('en-US', {
            hour12: false,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        })
    }
    // yesterday
    if (days_between === 1) {
        return `Yesterday ` + date.toLocaleTimeString('en-US', {
            hour12: false,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        })
    }
    // in same week
    if (days_between <= (today_week_day - 1)) {
        return `${days_between} days ago ` + date.toLocaleTimeString('en-US', {
            hour12: false,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        })
    }
    // last week
    if (days_between <= (today_week_day - 1 + 7)) {
        return `Last week ${date_week_day} ` + date.toLocaleTimeString('en-US', {
            hour12: false,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        })
    }
    const formattedTime = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}:${date.getSeconds().toString().padStart(2, '0')}`;
    return formattedTime;
}

export function RecentUpdatesPage() {
    const [bangumiIndex, setBangumiIndex] = useState(new BangumiIndex());
    const [trackerData, setTrackerData] = useState(new Map<number, SHARE_DMHY_ORG_TRACKER_CONFIG>());
    const [updatedBangumi, setUpdatedBangumi] = useState(new Array<Bangumi>());
    useEffect(() => {
        Promise.all([getBangumiIndex(), getDMHYTrackerData()]).
            then(([bangumi_index_resp, dmhy_tracker_data]) => {
                const dict = new Map<number, SHARE_DMHY_ORG_TRACKER_CONFIG>();
                dmhy_tracker_data.data.configs.forEach((cfg) => {
                    dict.set(cfg.bangumi_id, cfg);
                });
                setTrackerData(dict);
                setBangumiIndex(bangumi_index_resp.data);
            });
    }, []);

    useEffect(() => {
        const indexes = bangumiIndex.index.filter((b) => trackerData.has(b.id));
        indexes.sort((a, b) => {
            let a_timestamp = new Date(trackerData.get(a.id)?.latest_update_time || 0).getTime();
            let b_timestamp = new Date(trackerData.get(b.id)?.latest_update_time || 0).getTime();
            return a_timestamp - b_timestamp;
        }).reverse();
        setUpdatedBangumi(Array.from(indexes));
    }, [trackerData, bangumiIndex]);

    return (
        <Container maxWidth="lg" sx={{ color: 'rgb(138, 54, 49)' }}>
            <Box>
                <Timeline
                    sx={{
                        [`& .${timelineOppositeContentClasses.root}`]: {
                            flex: 0,
                        },
                    }}
                >
                    {updatedBangumi.map((anime: Bangumi, index: number) => (
                        <TimelineItem key={index}>
                            <TimelineOppositeContent color="textSecondary">
                                <Typography variant="overline" component="span" sx={{ lineHeight: '1rem' }}>
                                    {getDateString(trackerData.get(anime.id)?.latest_update_time || "")}
                                </Typography>
                            </TimelineOppositeContent>
                            <TimelineSeparator sx={{ height: '6em' }}>
                                <TimelineDot color="pink">
                                    <UpdateIcon sx={{ color: 'rgb(138, 54, 49)' }} />
                                </TimelineDot>
                                {index != updatedBangumi.length - 1 ? <TimelineConnector sx={{ backgroundColor: '#ff9b92' }} /> : <></>}
                            </TimelineSeparator>
                            <TimelineContent>
                                <Link key={anime.id} href={"/bangumi/" + anime.id} color="inherit" underline="none" display="block" className="w-fit">
                                    <Typography variant="h6" className="mt-2 underline underline-offset-4 w-fit">
                                        {anime.names[0].name}
                                    </Typography>
                                </Link>
                            </TimelineContent>
                        </TimelineItem>
                    ))}
                </Timeline>
            </Box>
        </Container >
    )
}