-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser 
-- that computes and store the average weighted score for a student.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (user_id INT)
BEGIN
    DECLARE total_score INT DEFAULT 0;
    DECLARE projects_count INT DEFAULT 0;

    SELECT SUM(corrections.score * projects.weight ), SUM(projects.weight)
        INTO total_score, projects_count
        FROM corrections
        LEFT JOIN projects ON ( projects.id = corrections.project_id )
        WHERE corrections.user_id = user_id;

    UPDATE users
        SET users.average_score = IF(projects_count = 0, 0, total_score / projects_count)
        WHERE users.id = user_id;
END $$
DELIMITER ;