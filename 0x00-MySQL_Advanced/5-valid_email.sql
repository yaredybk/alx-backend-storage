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
      SET @base = REGEXP_REPLACE(NEW.`email`, '\\+.*@','@');
      IF @base != OLD.`email` THEN
        SET NEW.`valid_email` = 0;
      END IF;
    END;
  END IF;
END//
DELIMITER ;