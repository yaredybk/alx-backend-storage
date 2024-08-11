-- Write a SQL script that creates a trigger
-- that resets the attribute valid_email
-- only when the email has been changed.
DELIMITER //

CREATE TRIGGER `invalidate_email` AFTER UPDATE ON `users`
FOR EACH ROW 
BEGIN
  IF NEW.`email` IS NULL THEN
    SET NEW.`valid_email` = 0;
  ELSEIF NEW.`email` != OLD.`email` THEN
    BEGIN
      SET @e1 = REGEXP_REPLACE(NEW.`email`, '\\+.*@','@');
      SET @e2 = REGEXP_REPLACE(OLD.`email`, '\\+.*@','@');
      IF @e1 != @e2 THEN
        SET NEW.`valid_email` = 0;
      END IF;
    END;
  END IF;
END//
DELIMITER ;