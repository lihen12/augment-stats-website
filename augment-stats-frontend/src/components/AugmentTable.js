// AugmentTable.js
import React from 'react';

const AugmentTable = ({ augments }) => {
    return (
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Games Played</th>
                    <th>Average Placement</th>
                    <th>Placement at 2-1</th>
                    <th>Placement at 3-2</th>
                    <th>Placement at 4-2</th>
                </tr>
            </thead>
            <tbody>
                {augments.map(augment => (
                    <tr key={augment.name}>
                        <td>{augment.name}</td>
                        <td>{augment.times_played}</td>
                        <td>{augment.average_placement}</td>
                        <td>{augment.placement_2_1}</td>
                        <td>{augment.placement_3_2}</td>
                        <td>{augment.placement_4_2}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default AugmentTable;
