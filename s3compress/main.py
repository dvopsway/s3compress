import click
import os
import sys
import math
import boto
import bz2
import json
import commands
from os import path
from multiprocessing import Pool
from boto.s3.prefix import Prefix
from boto.s3.key import Key
import psutil

delimiter = '/'
compressionLevel = 9


def upload_file(s3, bucketname, file_path, prefix):
    b = s3.get_bucket(bucketname)
    filename = os.path.basename(file_path)
    k = b.new_key(prefix + "/" + filename)
    mp = b.initiate_multipart_upload(prefix + "/" + filename)
    source_size = os.stat(file_path).st_size
    bytes_per_chunk = 5000 * 1024 * 1024
    chunks_count = int(math.ceil(source_size / float(bytes_per_chunk)))
    for i in range(chunks_count):
        offset = i * bytes_per_chunk
        remaining_bytes = source_size - offset
        bytes = min([bytes_per_chunk, remaining_bytes])
        part_num = i + 1
        print "uploading part " + str(part_num) + " of " + str(chunks_count)
        with open(file_path, 'r') as fp:
            fp.seek(offset)
            mp.upload_part_from_file(fp=fp, part_num=part_num, size=bytes)
    if len(mp.get_all_parts()) == chunks_count:
        mp.complete_upload()
        return True
    else:
        mp.cancel_upload()
        return False


def compress_file(filepath):
    destination_file = "%s.bz2" % filepath
    tarbz2contents = bz2.compress(
        open(filepath, 'rb').read(), compressionLevel)
    fh = open(destination_file, "wb")
    fh.write(tarbz2contents)
    fh.close()
    print "%s successfully created." % destination_file
    return destination_file


def list_files(bucket,destination_bucket, prefix, access, secret):
    files = []
    out = commands.getstatusoutput(
        "AWS_ACCESS_KEY_ID=%s AWS_SECRET_ACCESS_KEY=%s aws s3 ls --recursive s3://%s/%s | awk '{print $4}'" % (access, secret, bucket, prefix))
    if out[0] == 0:
        for each in out[1].split("\n"):
            if each[-1:] != "/":
                pair = []
                tokens = each.split("/")
                pair.append(tokens[len(tokens) - 1])
                del tokens[len(tokens) - 1]
                pair.append("/".join(tokens))
                pair.append(access)
                pair.append(secret)
                pair.append(bucket)
                pair.append(destination_bucket)
                files.append(pair)
    return files


def fetch_file(bucket, file_name, prefix, access, secret):
    out = commands.getstatusoutput(
        "AWS_ACCESS_KEY_ID=%s AWS_SECRET_ACCESS_KEY=%s aws s3 cp s3://%s/%s/%s /tmp | awk '{print $4}'" % (access, secret, bucket, prefix, file_name))
    if out[0] == 0:
        print "%s/%s downloaded in /tmp" % (prefix, file_name)
        return "/tmp/%s" % file_name
    else:
        print out
        return None

def process_file(uploaddata):
    file_name = uploaddata[0]
    prefix = uploaddata[1]
    access_key = uploaddata[2]
    secret_key = uploaddata[3]
    bucket_name = uploaddata[4]
    destination_bucket = uploaddata[5]

    s3 = boto.connect_s3(access_key, secret_key)
    print "Downloading file %s/%s locally"%(prefix,file_name)
    temp_path = fetch_file(bucket_name, file_name, prefix, access_key, secret_key)
    compressed_path = compress_file(temp_path)
    if upload_file(s3, destination_bucket, compressed_path, prefix):
        print "Successfully uploaded to s3://%s/%s/%s, removing local files" % (destination_bucket,prefix,os.path.basename(compressed_path))
        os.remove(temp_path)
        os.remove(compressed_path)
        print "%s uploaded" % compressed_path
    else:
        print "upload failed for %s/%s,removing local files" %(prefix,file_name)
        os.remove(temp_path)
        os.remove(compressed_path)

@click.command()
@click.option('--access_key', '-a', help='aws access_key')
@click.option('--secret_key', '-s', help='aws secret_key')
@click.option('--bucket_name', '-b', help='s3 bucket name')
@click.option('--destination_bucket', '-d', help='destination s3 bucket name')
@click.option('--prefix', '-p', default = "",help='s3 prefix')
@click.option('--workers', '-w', default = psutil.cpu_count() ,help='number of workers')
def main(access_key, secret_key, bucket_name,destination_bucket , prefix,workers):
    s3 = boto.connect_s3(access_key, secret_key)
    output = list_files(bucket_name, destination_bucket, prefix, access_key, secret_key)
    p = Pool(workers)
    p.map(process_file, output)
